from aiogram import types
from aiogram.dispatcher import FSMContext

from telegram_bot_app.core import dispatcher


@dispatcher.message_handler(commands='start')
async def cmd_start(message: types.Message, state: FSMContext):
    """Work with command start."""

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Отменить уроки', 'Перенести уроки')

    await message.reply('Что ты хочешь сделать.', reply_markup=markup)
