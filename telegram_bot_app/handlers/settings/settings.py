from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loguru import logger

from telegram_bot_app.core import dispatcher
from telegram_bot_app.functions import create_new_user, get_user_by_chat_id
from telegram_bot_app.functions.settings import create_message_settings


@dispatcher.message_handler(commands='settings')
@dispatcher.message_handler(Text(equals='settings', ignore_case=True))
async def cmd_settings(message: types.Message, state: FSMContext):
    """Work with command settings."""
    chat_id = message.from_id
    logger.configure(extra={'chat_id': chat_id, 'work_id': datetime.now().timestamp()})
    logger.debug(f'message = {message}')

    user = await get_user_by_chat_id(chat_id=chat_id)

    if not user:
        await create_new_user(chat_id=chat_id, name=message.from_user.first_name, message=message)
        return

    await create_message_settings(user=user, message=message)

