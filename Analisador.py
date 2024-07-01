from Webdriver import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import *

import time
import asyncio
import requests

class Analisador:
    def __init__(self, tokenID='', chatID='', tag='') -> None:
        self.driver = None
        self.limitNumbers = 200
        self.dataset = []
        self.green_counter = 0
        self.counter = 0
        self.wait = 0
        
        self.tag = tag

        self.API_KEY = tokenID
        self.chatID = chatID

        self.hasGreen = False

        self.MAX_VALUE = 10
        self.next20 = []
        self.maxLen = 10

        self.GREEN_COUNT = 0
        self.LOSS_COUNT = 0

        self.sendMessage('Iniciando execução!')
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
  
    def register(self, text):
        try:
            with open("logs.txt", "a") as file:
                file.write(text + "\n")
        except Exception as e:
            print(f"Ocorreu um erro ao registrar o texto: {e}")

    def hasNewNumber(self):
        try:
            self.driver.execute_script("""document.getElementsByClassName("lucide lucide-x h-5 w-5")[0]?.parentElement?.click()""")
        except Exception as e:
            print('.', e)
        allNumbers = self.driver.execute_script("return document.querySelectorAll('button.cell');")
        lastNumber = allNumbers[0]
        text_content = self.driver.execute_script("return [arguments[0].children[0].textContent, arguments[0].children[1].textContent]", lastNumber)
        value, index, _time = self.__format_number(text_content)
    
        new_number = value != self.dataset[0]['value'] and _time != self.dataset[0]['time']

        return new_number, (value, index, _time)

    def sendMessage(self, message, telegram=True):
        message = self.tag + ': ' + str(message)
        self.register(str(message))
        if telegram:
            url = f"https://api.telegram.org/bot{self.API_KEY}/sendMessage"
            params = {
                "chat_id": self.chatID,
                "text": message
            }

            requests.get(url, params=params)

    def analyze_next_20(self):
        hasOcorredGreen = False

        while len(self.next20) < self.maxLen:
            time.sleep(1)
            new_number, _data = self.hasNewNumber()

            if not new_number:
                continue

            _dict = {
                'value': _data[0],
                'index': float(_data[1]),
                'time': _data[2],
            }

            self.dataset.insert(0, _dict)
        
            if len(self.next20) < self.maxLen:
                self.next20.append(_dict)

                if _dict['value'] >= self.MAX_VALUE:
                    hasOcorredGreen = True
                    if self.green_counter >= 1:
                        self.sendMessage(f"GREEN {_dict['value']}")
                        self.GREEN_COUNT += 1
                    self.green_counter += 1
                    if self.green_counter == 1:
                        self.sendMessage(f'FIQUE ATENTO(A) AO JOGO: {_dict["value"]}')
                    break
    
        if len(self.next20) >= self.maxLen and not hasOcorredGreen:
            if self.green_counter > 0:
                self.sendMessage("LOSS")
                self.LOSS_COUNT += 1
                self.green_counter = 0 

        self.next20 = []

        pass

    def __analyze(self):
        while True:
            time.sleep(1)
            new_number, _data = self.hasNewNumber()

            if not new_number:
                continue

            _dict = {
                'value': _data[0],
                'index': _data[1],
                'time': _data[2]
            }

            self.dataset.insert(0, _dict)

            print(f"{self.tag}: {_dict['value']}")

            if self.wait > 0:
                self.wait -= 1
                continue
            
            self.counter = 0

            data = self.dataset
            last_16 = data[0:16]
            last_15 = data[1:16]
            last_5 = last_16[0:5]
            last_4 = last_16[0:4]

            greens = [num for num in last_16 if self.classify_number(num['value']) == 'verde']
            green_percentage = len(greens) / 16

            grays = [num for num in last_16 if self.classify_number(num['value']) == 'cinza']
            gray_percentage = len(grays) / 16

            last_15_greens = [num for num in last_15 if self.classify_number(num['value']) == 'verde']
            last_15_green_percentage = len(last_15_greens) / 15

            last_15_grays = [num for num in last_15 if self.classify_number(num['value']) == 'cinza']
            last_15_gray_percentage = len(last_15_grays) / 15

            if last_15_green_percentage > 0.72 and all(self.classify_number(num['value']) == 'verde' for num in last_4):
                if self.green_counter >= 1:
                    self.sendMessage('ANALISANDO VERDE ', _dict['value'])

            if green_percentage > 0.74 and all(self.classify_number(num['value']) == 'verde' for num in last_5):
                if self.green_counter >= 1:
                    self.sendMessage('AUTORIZADO VERDE ', _dict['value'])
                self.analyze_next_20()

            if last_15_gray_percentage > 0.72 and all(self.classify_number(num['value']) == 'cinza' for num in last_4):
                if self.green_counter >= 1:
                    self.sendMessage('ANALISANDO CINZA', _dict['value'])

            if gray_percentage > 0.74 and all(self.classify_number(num['value']) == 'cinza' for num in last_5):
                if self.green_counter >= 1:
                    self.sendMessage('AUTORIZADO CINZA', _dict['value'])
                self.analyze_next_20()

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

        print(len(self.dataset))
        
        self.__analyze()