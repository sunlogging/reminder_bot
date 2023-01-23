import asyncio
import logging
import os

import aioschedule as aioschedule
from aiogram import types, Bot, Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv('.env')
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('API_TOKEN'))
dp = Dispatcher(bot)
task = []

for t in os.getenv('TASK').split(')'):
    if len(t.split('(')) > 1:
        task.append(t.split('(')[1])


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


async def send_reminder():
    for user in os.getenv('IDS').split(' '):
        await bot.send_message(user, f'<b>{task[1]}</b>\n<i>{task[2]}</i>', parse_mode='HTML')



async def scheduler():
    aioschedule.every().day.at(f"{task[0].split(':')[0]}:{task[0].split(':')[1]}").do(send_reminder)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dp):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
