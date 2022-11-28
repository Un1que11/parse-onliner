import os
import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink

from parse_onliner.main import collect_data


bot = Bot(token=os.getenv('TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Notebooks']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Discounted items', reply_markup=keyboard)


@dp.message_handler(Text(equals='Notebooks'))
async def get_discount_notebook(message: types.Message):
    await message.answer('Please waiting...')

    collect_data()

    with open('result_data.json') as f:
        data = json.load(f)

    for item in data:
        card = f'{hlink(item.get("title"), item.get("link"))}\n' \
               f'{hbold("Price: ")} {item.get("price_base")}\n' \
               f'{hbold("Discount price: ")} {item.get("discount_percent")}%: {item.get("price_sale")}🥶'

        await message.answer(card)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
