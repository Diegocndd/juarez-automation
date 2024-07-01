from Analisador import *
from utils import *

import threading

blazejapt_bot = '7354343346:AAEx28mOyUQ7N2FbWfIdmCUvgNny-KHTFVI'
jonbetjapt_bot = '7270628841:AAF6AmUvcaThAOx4nmCxyu-rai27Dd85k7g'

JONBET_GROUP_ID = '-4247320411'
BLAZE_GROUP_ID = '-4264305485'

def init_analisador(analisador, url):
    analisador.init(url)

A1 = Analisador(chatID=JONBET_GROUP_ID, tokenID=jonbetjapt_bot, tag='JonBet - Crash')
A2 = Analisador(chatID=JONBET_GROUP_ID, tokenID=jonbetjapt_bot, tag='JonBet - Crash2')
A3 = Analisador(chatID=JONBET_GROUP_ID, tokenID=jonbetjapt_bot, tag='JonBet - Aviator')
B1 = Analisador(chatID=BLAZE_GROUP_ID, tokenID=blazejapt_bot, tag='Blaze - Aviator')
B2 = Analisador(chatID=BLAZE_GROUP_ID, tokenID=blazejapt_bot, tag='Blaze - Crash')
B3 = Analisador(chatID=BLAZE_GROUP_ID, tokenID=blazejapt_bot, tag='Blaze - Crash2')

threads = []

threads.append(threading.Thread(target=init_analisador, args=(A1, CRASH_JONBET_URL)))
threads.append(threading.Thread(target=init_analisador, args=(A2, CRASH2_JONBET_URL)))
threads.append(threading.Thread(target=init_analisador, args=(A3, AVIATOR_JONBET_URL)))
threads.append(threading.Thread(target=init_analisador, args=(B1, CRASH_BLAZE_URL)))
threads.append(threading.Thread(target=init_analisador, args=(B2, CRASH2_BLAZE_URL)))
threads.append(threading.Thread(target=init_analisador, args=(B3, AVIATOR_BLAZE_URL)))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()