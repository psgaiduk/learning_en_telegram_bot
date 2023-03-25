from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loguru import logger

from telegram_bot_app.core import dispatcher
from telegram_bot_app.functions import get_user_by_chat_id
from telegram_bot_app.states import SettingsStates


@dispatcher.message_handler(commands='settings')
@dispatcher.message_handler(Text(equals='settings', ignore_case=True))
async def cmd_settings(message: types.Message, state: FSMContext):
    """Work with command settings."""
    chat_id = message.from_id
    logger.configure(extra={'chat_id': chat_id, 'work_id': datetime.now().timestamp()})
    logger.debug(f'message = {message}')

    user = await get_user_by_chat_id(chat_id=chat_id, name=message.from_user.first_name)

    await SettingsStates.start_settings.set()

    level_0 = types.InlineKeyboardButton('Детский', callback_data='level_0')
    level_1 = types.InlineKeyboardButton('1', callback_data='level_1')
    level_2 = types.InlineKeyboardButton('2', callback_data='level_2')
    level_3 = types.InlineKeyboardButton('3', callback_data='level_3')
    cancel = types.InlineKeyboardButton('Завершить', callback_data='cancel')

    if user.level == 0:
        start_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True).add(level_1, level_2, level_3, cancel)
    elif user.level == 1:
        start_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True).add(level_0, level_2, level_3, cancel)
    elif user.level == 2:
        start_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True).add(level_0, level_1, level_3, cancel)
    else:
        start_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True).add(level_0, level_1, level_2, cancel)

    answer_text = f'{user.name}, вот твои настройки:\nУровень сложности: {user.level}'
    await message.answer(answer_text, reply_markup=start_keyboard, parse_mode='HTML')
