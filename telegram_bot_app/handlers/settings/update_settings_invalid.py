from aiogram import types

from telegram_bot_app.core import dispatcher
from telegram_bot_app.states import SettingsStates


@dispatcher.message_handler(state=SettingsStates.start_settings)
async def update_settings_invalid(message: types.Message):
    """
    If next sentence is invalid
    """
    text_message = 'Завершите настройку'

    return await message.reply(text_message)
