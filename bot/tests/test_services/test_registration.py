from http import HTTPStatus

from aiohttp import ClientResponse
from pytest import mark
from unittest.mock import AsyncMock, Mock, patch

from settings import settings
from services import RegistrationService


class TestRegistrationService:
    """Tests for RegistrationService."""

    @classmethod
    def setup_class(cls):
        cls._message = Mock()
        cls._message.from_user.id = 12345
        cls._post_method_target = "context_managers.aio_http_client.AsyncHttpClient.post"

    @mark.asyncio
    async def test_create_user(self, mocker):
        self._message.answer = AsyncMock()
        self._service = RegistrationService(message=self._message)

        with patch(self._post_method_target, return_value=({}, HTTPStatus.CREATED)) as mocked_post:
            await self._service._create_user()

        mocked_post.assert_awaited_once_with(
            url=f"{settings.api_url}/v1/telegram_user/",
            headers=settings.api_headers,
            json={
                "telegram_id": 12345,
                "main_language_id": 1,
                "experience": 0,
                "hero_level_id": 1,
                "previous_stage": "NEW_CLIENT",
                "stage": "WAIT_NAME",
            },
        )

        self._message.answer.assert_not_called()

    @mark.asyncio
    async def test_create_user_mistake(self):
        self._message.answer = AsyncMock()
        self._service = RegistrationService(message=self._message)

        with patch(self._post_method_target, return_value=({}, HTTPStatus.NOT_FOUND)) as mocked_post:
            await self._service._create_user()

        mocked_post.assert_awaited_once_with(
            url=f"{settings.api_url}/v1/telegram_user/",
            headers=settings.api_headers,
            json={
                "telegram_id": 12345,
                "main_language_id": 1,
                "experience": 0,
                "hero_level_id": 1,
                "previous_stage": "NEW_CLIENT",
                "stage": "WAIT_NAME",
            },
        )

        self._message.answer.assert_called_once_with("🤖 Что-то пошло не так. Попробуйте еще раз, чуть позже.")

    @mark.asyncio
    async def test_send_greeting_message(self):
        self._message.answer = AsyncMock()
        self._service = RegistrationService(message=self._message)

        await self._service._send_greeting_message()

        self._message.answer.assert_called_once_with(
            "👋 Добро пожаловать!\n\n"
            f"Вот ссылка, чтобы пригласить друзей: https://t.me/{settings.bot_name}?start=rfu\n\n"
            "📝 Пожалуйста, введи своё имя чтобы продолжить регистрацию."
        )

    @mark.asyncio
    async def test_create_referral(self):
        self._message.text = "/start a"
        self._message.answer = AsyncMock()
        self._service = RegistrationService(message=self._message)
        response_mock = AsyncMock(spec=ClientResponse)

        with patch(self._post_method_target, return_value=response_mock) as mocked_post:
            await self._service._create_referral()

        mocked_post.assert_awaited_once_with(
            url=f"{settings.api_url}/v1/referrals/",
            headers=settings.api_headers,
            json={
                "telegram_user_id": 1,
                "friend_telegram_id": 12345,
            },
        )

    @mark.asyncio
    async def test_not_create_referral_without_link(self):
        self._message.text = "/start"
        self._message.answer = AsyncMock()
        self._service = RegistrationService(message=self._message)
        response_mock = AsyncMock(spec=ClientResponse)

        with patch(self._post_method_target, return_value=response_mock) as mocked_post:
            await self._service._create_referral()

        mocked_post.assert_not_called()

    @mark.asyncio
    async def test_not_create_referral_without_link_with_message(self):
        self._message.text = "/start 123"
        self._message.answer = AsyncMock()
        self._service = RegistrationService(message=self._message)
        response_mock = AsyncMock(spec=ClientResponse)

        with patch(self._post_method_target, return_value=response_mock) as mocked_post:
            await self._service._create_referral()

        mocked_post.assert_not_called()
