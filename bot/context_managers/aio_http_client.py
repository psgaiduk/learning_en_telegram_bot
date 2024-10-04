from typing import Any, Optional

from aiohttp import ClientSession, ClientResponseError
from backoff import expo, on_exception
from contextlib import asynccontextmanager


class AsyncHttpClient:
    """Асинхронный HTTP клиент для выполнения запросов к API"""

    def __init__(self) -> None:
        """Init."""
        self.session = ClientSession()

    @on_exception(expo, ClientResponseError, max_tries=3)
    async def _request(self, method: str, url: str, **kwargs) -> tuple[Optional[Any], Optional[int]]:
        """Выполнение запроса к API."""
        try:
            async with self.session.request(method, url, **kwargs) as response:
                return await response.json(), response.status
        except ClientResponseError as e:
            print(f"HTTP Error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None, None

    async def get(self, url, headers=None, params=None):
        """Выполнение GET запроса к API."""
        return await self._request("GET", url, headers=headers, params=params)

    async def post(self, url, headers=None, json=None):
        """Выполнение POST запроса к API."""
        return await self._request("POST", url, headers=headers, json=json)

    async def patch(self, url, headers=None, json=None):
        """Выполнение PATCH запроса к API."""
        return await self._request("PATCH", url, headers=headers, json=json)

    async def close(self):
        """Закрытие сессии."""
        await self.session.close()


@asynccontextmanager
async def http_client():
    """Контекстный менеджер для асинхронного HTTP клиента."""
    client = AsyncHttpClient()
    try:
        yield client
    finally:
        await client.close()
