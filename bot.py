import logging

from aiogram import types, filters
from aiogram.utils.executor import start_webhook

from dispatcher import dp, bot
from fixer_currency.fixer_currency import lst, convert, history
from config import WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_PORT, WEBAPP_HOST


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['exchange ([0-9]*) ([\w]*) to ([\w]*)']))
async def exchange(message: types.Message, regexp_command):
    response = convert(regexp_command.group(1), regexp_command.group(2), regexp_command.group(3))
    await message.answer(response)


@dp.message_handler(commands='list', commands_prefix='/')
async def list(message: types.Message):
    response = lst()
    await message.answer(response)


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['history ([\w]*)/([\w]*) for ([0-9]*) days']))
async def stats(message: types.Message, regexp_command):
    response = history(regexp_command.group(1), regexp_command.group(2), regexp_command.group(3))
    await bot.send_photo(message.from_user.id, open(response, 'rb'), f'График за последние {regexp_command.group(3)} дней')


@dp.message_handler(commands='start', command_prefix='/')
async def welcome(message: types.Message):
    await message.answer('Im working')


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(dp)


async def on_shutdown(dp):
    logging.info(dp)


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
