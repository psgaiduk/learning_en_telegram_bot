from loguru import logger

from db.functions.users import get_user_by_telegram_id, create_user
from db.models import Users


async def get_user_by_chat_id(chat_id: int, name: str) -> Users:
    user = await get_user_by_telegram_id(telegram_id=chat_id)
    logger.debug(f'Get user = {user}')
    if not user:
        logger.debug(f'We don\'t have this user, create new user.')
        user = await create_user(telegram_id=chat_id, name=name)
        logger.debug(f'New user = {user}')
    return user
