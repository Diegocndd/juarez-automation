from enum import Enum
from typing import Type
    
CRASH_BLAZE_URL='https://www.tipminer.com/historico/blaze/crash'
CRASH2_BLACK_URL='https://www.tipminer.com/historico/blaze/crash2'

class Status(Enum):
    SUCCESS = 1
    FAILURE = 2
    PENDING = 3

def classify_number(num):
    """Classifica o número como cinza ou verde."""
    if 0 <= num <= 1.99:
        return 'cinza'
    elif 2 <= num <= 99999999:
        return 'verde'
    return 'indefinido'

def getTelegramMessage(key: str) -> str:
    if key == 'ANALIZANDO_VERDE':
        return 'Analisando Entrada (Verde)'
    elif key == 'AUTORIZADA_VERDE':
        return 'Entrada Autorizada (Verde)'
    elif key == 'ANALIZANDO_CINZA':
        return 'Analisando Entrada (Cinza)'
    elif key == 'AUTORIZADA_CINZA':
        return 'Entrada Autorizada (Cinza)'
    return ''