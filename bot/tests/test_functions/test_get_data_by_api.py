from http import HTTPStatus
from unittest.mock import AsyncMock, patch

from pytest import mark

from bot import bot
from functions import get_data_by_api_func
from settings import settings


class TestGetDataByApiFunction:
    """Tests for update_user function."""

    @classmethod
    def setup_class(cls):
        cls._telegram_id = 12345
        cls._get_method_target = "context_managers.aio_http_client.AsyncHttpClient.get"

    @mark.asyncio
    async def test_successful_get_data(self):
        return_value = {"detail": {"data": "ok"}}
        with patch(target=self._get_method_target, return_value=(return_value, HTTPStatus.OK)) as mocked_get:
            with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:
                result = await get_data_by_api_func(
                    telegram_id=self._telegram_id,
                    params_for_get={"id": 1},
                    url_for_get=f"telegram_user/{self._telegram_id}",
                )

        mocked_get.assert_awaited_once_with(
            url=f"{settings.api_url}/v1/telegram_user/{self._telegram_id}/",
            headers=settings.api_headers,
            params={"id": 1},
        )

        mock_send_message.assert_not_awaited()

        assert result == {"data": "ok"}

    @mark.asyncio
    async def test_not_successful_get_data(self):

        with patch(target=self._get_method_target, return_value=({}, HTTPStatus.NOT_FOUND)) as mocked_get:
            with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:
                result = await get_data_by_api_func(
                    telegram_id=self._telegram_id,
                    params_for_get={},
                    url_for_get=f"telegram_user/{self._telegram_id}",
                )

        mocked_get.assert_awaited_once_with(
            url=f"{settings.api_url}/v1/telegram_user/{self._telegram_id}/",
            headers=settings.api_headers,
            params={},
        )

        mock_send_message.assert_called_once_with(
            chat_id=self._telegram_id,
            text="🤖 Что-то пошло не так. Попробуйте еще раз, чуть позже.",
        )

        assert result is None
