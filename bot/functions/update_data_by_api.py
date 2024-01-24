from http import HTTPStatus

from context_managers import http_client
from bot import bot
from settings import settings


async def update_data_by_api(telegram_id: int, params_for_update: dict, url_for_update: str) -> bool:
    """
    Update telegram user status.

    :param telegram_id: telegram id.
    :param params_for_update: Dict with params for update user by api.
    :param url_for_update: Url for update user by api.
    :return: True or False
    """
    async with http_client() as client:
        url_update_telegram_user = f'{settings.api_url}/v1/{url_for_update}/'

        _, response_status = await client.patch(
            url=url_update_telegram_user,
            headers=settings.api_headers,
            json=params_for_update,
        )

    if response_status != HTTPStatus.OK:
        message_text = '🤖 Что-то пошло не так. Попробуйте еще раз, чуть позже.'
        await bot.send_message(chat_id=telegram_id, text=message_text)
        return False

    return True
