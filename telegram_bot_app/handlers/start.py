from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from telegram_bot_app.core import dispatcher


@dispatcher.message_handler(commands='start')
async def cmd_start(message: types.Message, state: FSMContext):
    """Work with command start."""
    chat_id = message.from_id
    logger.configure(extra={'chat_id': chat_id, 'work_id': datetime.now().timestamp()})
    logger.debug(f'message = {message}')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Отменить уроки', 'Перенести уроки')

    await message.reply('Что ты хочешь сделать.', reply_markup=markup)
