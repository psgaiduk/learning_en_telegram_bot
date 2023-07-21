from aiogram import types
from loguru import logger

from bot.bot import get_user_by_telegram_id, create_user
from db.models import Users
from telegram_bot_app.functions.settings import create_message_settings


async def get_user_by_chat_id(chat_id: int) -> Users:
    user = await get_user_by_telegram_id(telegram_id=chat_id)
    logger.debug(f'Get user = {user}')

    return user


async def create_new_user(chat_id: int, name: str, message: types.Message):
    logger.debug(f'We don\'t have this user, create new user.')
    user = await create_user(telegram_id=chat_id, name=name)
    logger.debug(f'New user = {user}')

    await create_message_settings(user=user, message=message)
