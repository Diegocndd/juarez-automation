from Webdriver import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import *
from telegram import send_message

import time
import asyncio
class Analisador:
    def __init__(self, group: str) -> None:
        self.driver = None
        self.limitNumbers = 200
        self.dataset = []
        self.green_counter = 0
        self.ANALYSIS_STATE = None
        self.next20 = []
        self.wait = 0
        self.MAX_VALUE = 30
        self.telegramGroup = group
        pass

    def init(self, url: str) -> None:
        self.driver = Webdriver('.').getDriver()
        self.driver.get(f"{url}?limit={self.limitNumbers}")
        time.sleep(20)
        self.__populate_database()

    def classify_number(self, num):
        """Classifica o número como cinza ou verde."""
        if 0 <= num <= 1.99:
            return 'cinza'
        elif 2 <= num <= 99999999:
            return 'verde'
        return 'indefinido'

    def compute_alert(self) -> str:
        if len(self.dataset) < 36:
            return False
                
        data = self.dataset
        last_16 = data[0:16]  # Últimos 16 Resultados
        last_15 = data[1:16]  # Últimos 15 Resultados
        # last_5 = last_16[-5:]  # Últimos 5 Resultados
        # last_4 = last_16[-4:]  # Últimos 4 Resultados
        last_5 = last_16[0:5]  # Últimos 5 Resultados
        last_4 = last_16[0:4]  # Últimos 4 Resultados

        # Filtra os números verdes
        greens = [num for num in last_16 if self.classify_number(num['value']) == 'verde']
        green_percentage = len(greens) / 16

        # Filtra os números cinzas
        grays = [num for num in last_16 if self.classify_number(num['value']) == 'cinza']
        gray_percentage = len(grays) / 16
        # print('>', gray_percentage)
        # Filtra os números verdes nos últimos 15 resultados
        last_15_greens = [num for num in last_15 if self.classify_number(num['value']) == 'verde']
        last_15_green_percentage = len(last_15_greens) / 15

        # Filtra os números cinzas nos últimos 15 resultados
        last_15_grays = [num for num in last_15 if self.classify_number(num['value']) == 'cinza']
        last_15_gray_percentage = len(last_15_grays) / 15

        print(green_percentage, gray_percentage)

        # Verifica se a porcentagem de verdes nos últimos 15 resultados é superior a 72% e os últimos 4 resultados são verdes
        if last_15_green_percentage > 0.72 and all(self.classify_number(num['value']) == 'verde' for num in last_4):
            if self.green_counter >= 1:
                return 'ANALIZANDO_VERDE'

        if green_percentage > 0.74 and all(self.classify_number(num['value']) == 'verde' for num in last_5):
            if self.green_counter >= 1:
                return 'AUTORIZADA_VERDE'
            print('123')
            self.ANALYSIS_STATE = 'VERIFY_NEXT_20'


        # Verifica se a porcentagem de cinzas nos últimos 15 resultados é superior a 72% e os últimos 4 resultados são cinzas
        if last_15_gray_percentage > 0.72 and all(self.classify_number(num['value']) == 'cinza' for num in last_4):
            if self.green_counter >= 1:
                return 'ANALIZANDO_CINZA'

        if gray_percentage > 0.74 and all(self.classify_number(num['value']) == 'cinza' for num in last_5):
            if self.green_counter >= 1:
                return 'AUTORIZADA_CINZA'
            print('456')
            self.ANALYSIS_STATE = 'VERIFY_NEXT_20'

        return ''
        
    def __analyze(self):
        while True:
            time.sleep(1)
            try:
                self.driver.execute_script("""document.getElementsByClassName("lucide lucide-x h-5 w-5")[0]?.parentElement?.click()""")
            except Exception as e:
                print('.', e)
            allNumbers = self.driver.execute_script("return document.querySelectorAll('button.cell');")
            lastNumber = allNumbers[0]
            text_content = self.driver.execute_script("return [arguments[0].children[0].textContent, arguments[0].children[1].textContent]", lastNumber)
            value, index, _time = self.__format_number(text_content)
       
            new_number = value != self.dataset[0]['value'] and _time != self.dataset[0]['time']

            if new_number:
                _dict = {
                    'index': index,
                    'value': value,
                    'time': _time
                }
                self.dataset.insert(0, _dict)

                print('NEW: ', _dict)

                if self.wait > 0:
                    self.wait -= 1
                    continue
                
                if self.ANALYSIS_STATE == 'VERIFY_NEXT_20':
                    print('>>', self.next20)
                    if len(self.next20) < 20:
                        self.next20.append(_dict)
                    else:
                        for num in self.next20:
                            if num['value'] > self.MAX_VALUE:
                                if self.green_counter >= 1:
                                    print(f"Green: {num}")
                                    asyncio.run(send_message(self.telegramGroup, f"Green: {num}"))
                                    self.wait = 13
                                self.green_counter += 1
                                if self.green_counter == 1:
                                    asyncio.run(send_message(self.telegramGroup, "FIQUE ATENTO(A) AO JOGO"))
                                    print("FIQUE ATENTO(A) AO JOGO")
                                break
                        else:
                            if self.green_counter >= 1:
                                print("Loss")
                                asyncio.run(send_message(self.telegramGroup, "LOSS"))
                                self.wait = 13
                                self.green_counter = 0
                        self.next20 = []
                        self.ANALYSIS_STATE = None
                else:     
                    res = self.compute_alert()
                    if res:
                        asyncio.run(send_message(self.telegramGroup, getTelegramMessage(res)))
                        print(getTelegramMessage(res))
                    else:
                        # asyncio.run(send_message(self.telegramGroup, 'PASSOU'))
                        # print('PASSOU...')
                        pass


    def __format_number(self, text_content):
        splitted = text_content[0].split('x')
        _time = text_content[1]

        result = splitted[0]
        index = splitted[1]

        return (float(result.replace(',', '.')), int(index), _time)

    def __populate_database(self) -> None:
        allNumbers = self.driver.execute_script("return document.querySelectorAll('button.cell');")

        for i in range(0, len(allNumbers)):
            try:
                text_content = self.driver.execute_script("return [arguments[0].children[0].textContent, arguments[0].children[1].textContent]", allNumbers[-i])

                value, index, time = self.__format_number(text_content)
                self.dataset.append({
                    'value': value,
                    'index': index,
                    'time': time
                })
            except Exception as e:
                print(e)
                pass
            # print()
        print(len(self.dataset))
        self.__analyze()