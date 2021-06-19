from aiogram import types, filters
from aiogram.utils import executor

from dispatcher import dp, bot
from fixer_currency.fixer_currency import lst, convert, history


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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
