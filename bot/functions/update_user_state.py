from http import HTTPStatus

from context_managers import http_client
from bot import bot
from settings import settings


async def update_user_state(telegram_id: int, state: str) -> bool:
    """
    Update telegram user status.

    :param telegram_id: telegram id.
    :param state: new state for user.
    :return:
    """
    async with http_client() as client:
        url_update_telegram_user = f'{settings.api_url}/v1/telegram_user/{telegram_id}'
        data_for_update_user = {
            'telegram_id': telegram_id,
            'stage': state,
        }
        _, response_status = await client.patch(
            url=url_update_telegram_user,
            headers=settings.api_headers,
            json=data_for_update_user,
        )

    if response_status != HTTPStatus.OK:
        message_text = '🤖 Что-то пошло не так. Попробуйте еще раз, чуть позже.'
        await bot.send_message(chat_id=telegram_id, text=message_text)
        return False

    return True
