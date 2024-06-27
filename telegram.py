from telethon import TelegramClient
from telethon.tl.types import InputPeerChannel, InputPeerChat

import os
import asyncio

api_id = 22878300
api_hash = '1ae533d7273bd5824e6a5a29c46cfc8f'

async def connect():
    if not api_id or not api_hash:
        return
    async with TelegramClient('name', api_id, api_hash) as client:
        destiny_channel = await client.get_entity('https://t.me/+YP_CcLvL2KYxMmFh')
        print(destiny_channel)
        return

# asyncio.run(connect())

def getChatId(group):
    return 4261896823

async def send_message(group, message):
    if not api_id or not api_hash:
        return
    destiny_group = InputPeerChat(chat_id=getChatId(group))
    async with TelegramClient('name', api_id, api_hash) as client:
        await client.send_message(destiny_group, message)

# asyncio.run(send_message('Hi!'))

