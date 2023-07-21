from aiogram import types

from db.models import Users
from main.choices import Levels
from bot.bot import SettingsStates


async def create_message_settings(user: Users, message: types.Message):
    """Create message settings."""

    await SettingsStates.start_settings.set()

    level_0 = types.InlineKeyboardButton(Levels.A1.name, callback_data='level_0')
    level_1 = types.InlineKeyboardButton(Levels.A2.name, callback_data='level_1')
    level_2 = types.InlineKeyboardButton(Levels.B1.name, callback_data='level_2')
    level_3 = types.InlineKeyboardButton(Levels.B2.name, callback_data='level_3')
    cancel = types.InlineKeyboardButton('Завершить', callback_data='cancel')

    if user.level == 0:
        start_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True).add(level_1, level_2, level_3, cancel)
    elif user.level == 1:
        start_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True).add(level_0, level_2, level_3, cancel)
    elif user.level == 2:
        start_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True).add(level_0, level_1, level_3, cancel)
    else:
        start_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True).add(level_0, level_1, level_2, cancel)

    level_name = Levels.get_level_name(level=user.level)

    answer_text = f'{user.name}, вот твои настройки:\nУровень сложности: {level_name}'
    await message.answer(answer_text, reply_markup=start_keyboard, parse_mode='HTML')
