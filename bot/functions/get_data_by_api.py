from http import HTTPStatus
from typing import Optional

from context_managers import http_client
from bot import bot
from settings import settings


async def get_data_by_api_func(telegram_id: int, params_for_get: dict, url_for_get: str) -> Optional[dict]:
    """
    Get data by api.

    :param telegram_id: telegram id.
    :param params_for_get: Dict with params for get data by api.
    :param url_for_get: Url for get data by api.
    :return: Data from api.
    """
    async with http_client() as client:
        url_for_get_data = f"{settings.api_url}/v1/{url_for_get}/"

        response, response_status = await client.get(
            url=url_for_get_data,
            headers=settings.api_headers,
            json=params_for_get,
        )

    if response_status != HTTPStatus.OK:
        message_text = "🤖 Что-то пошло не так. Попробуйте еще раз, чуть позже."
        await bot.send_message(chat_id=telegram_id, text=message_text)
        return None

    return response.get('detail')
