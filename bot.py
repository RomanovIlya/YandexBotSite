import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import WebAppInfo
from utils import read_json

logging.basicConfig(level=logging.INFO)

bot = Bot(token=read_json("BOT_TOKEN"))
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(
            text="Открыть кликер",
            web_app=WebAppInfo(url = f'{read_json("WEBAPP_URL")}/{message.from_user.id}')
        )
    )
    await message.answer(
        "Нажмите кнопку ниже, чтобы открыть кликер!",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

if __name__ == '__main__':
    from threading import Thread
    from app import app as flask_app
    
    flask_thread = Thread(target=flask_app.run, kwargs={
        'ssl_context': ('cert.pem', 'key.pem'),
        'host': read_json("WEBAPP_HOST"),
        'port': read_json("WEBAPP_PORT"),
        'debug': False,
        'use_reloader': False
    })
    flask_thread.start()
    
    asyncio.run(dp.start_polling(bot))