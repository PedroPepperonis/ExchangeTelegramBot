import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)
