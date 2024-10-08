from http import HTTPStatus
from unittest.mock import AsyncMock, patch

from pytest import mark

from bot import bot
from functions import update_data_by_api
from settings import settings


class TestUpdateUserFunction:
    """Tests for update_user function."""

    @classmethod
    def setup_class(cls):
        cls._telegram_id = 12345
        cls._patch_method_target = "context_managers.aio_http_client.AsyncHttpClient.patch"

    @mark.parametrize(
        "params_for_update",
        [
            {"stage": "WAIT_NAME"},
            {"stage": "WAIT_LEVEL"},
        ],
    )
    @mark.asyncio
    async def test_successful_update(self, params_for_update):

        with patch(target=self._patch_method_target, return_value=({}, HTTPStatus.OK)) as mocked_patch:
            with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:
                result = await update_data_by_api(
                    telegram_id=self._telegram_id,
                    params_for_update=params_for_update,
                    url_for_update=f"telegram_user/{self._telegram_id}",
                )

        mocked_patch.assert_awaited_once_with(
            url=f"{settings.api_url}/v1/telegram_user/{self._telegram_id}/",
            headers=settings.api_headers,
            json=params_for_update,
        )

        mock_send_message.assert_not_awaited()

        assert result is True

    @mark.asyncio
    async def test_not_successful_update(self):

        with patch(target=self._patch_method_target, return_value=({}, HTTPStatus.NOT_FOUND)) as mocked_patch:
            with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:
                result = await update_data_by_api(
                    telegram_id=self._telegram_id,
                    params_for_update={},
                    url_for_update=f"telegram_user/{self._telegram_id}",
                )

        mocked_patch.assert_awaited_once_with(
            url=f"{settings.api_url}/v1/telegram_user/{self._telegram_id}/",
            headers=settings.api_headers,
            json={},
        )

        mock_send_message.assert_called_once_with(
            chat_id=self._telegram_id,
            text="🤖 Что-то пошло не так. Попробуйте еще раз, чуть позже.",
        )

        assert result is False
