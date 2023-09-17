from aiogram import types

from telegram_bot_app.core import dispatcher


@dispatcher.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    await message.answer("Привет! Это ваш бот.")
