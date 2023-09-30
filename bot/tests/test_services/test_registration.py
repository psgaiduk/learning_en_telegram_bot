import pytest
from aiohttp import ClientResponse
from unittest.mock import AsyncMock, Mock, patch

from settings import settings
from services import RegistrationService


class TestRegistrationService:
    """Tests for RegistrationService."""

    @classmethod
    def setup_class(cls):
        cls._message = Mock()

    @pytest.mark.asyncio
    async def test_create_user(self):
        self._message.from_user.id = 12345
        self._message.answer = AsyncMock()
        self._service = RegistrationService(message=self._message)
        response_mock = AsyncMock(spec=ClientResponse)
        response_mock.status = 201

        with patch('context_managers.aio_http_client.AsyncHttpClient.post', return_value=response_mock) as mocked_post:
            await self._service._create_user()

        mocked_post.assert_awaited_once_with(
            url=f'{settings.api_url}/v1/telegram_user/',
            headers=settings.api_headers,
            json={
                'telegram_id': 12345,
                'level_en_id': 1,
                'main_language_id': 1,
                'experience': 0,
                'hero_level_id': 1,
                'previous_stage': '',
                'stage': 'WAIT_NAME',
            }
        )

        self._message.answer.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_user_mistake(self):
        self._message.from_user.id = 12345
        self._message.answer = AsyncMock()
        self._service = RegistrationService(message=self._message)
        response_mock = AsyncMock(spec=ClientResponse)
        response_mock.status = 404

        with patch('context_managers.aio_http_client.AsyncHttpClient.post', return_value=response_mock) as mocked_post:
            await self._service._create_user()

        mocked_post.assert_awaited_once_with(
            url=f'{settings.api_url}/v1/telegram_user/',
            headers=settings.api_headers,
            json={
                'telegram_id': 12345,
                'level_en_id': 1,
                'main_language_id': 1,
                'experience': 0,
                'hero_level_id': 1,
                'previous_stage': '',
                'stage': 'WAIT_NAME',
            }
        )

        self._message.answer.assert_called_once_with(
            '🤖 Что-то пошло не так. Попробуйте еще раз, чуть позже.'
        )

    @pytest.mark.asyncio
    async def test_send_greeting_message(self):
        self._message.from_user.id = 12345
        self._message.answer = AsyncMock()
        self._service = RegistrationService(message=self._message)

        await self._service._send_greeting_message()

        self._message.answer.assert_called_once_with(
            '👊 Добро пожаловать в Английский Клуб!\n\n'
            'Перед тем как начать, ты должен знать основные правила:\n\n'
            '1️⃣ Первое правило Английского Клуба: рассказывайте всем об Английском Клубе. '
            f'Отправьте https://t.me/{settings.bot_name}?start=rfu друзьям, чтобы они тоже могли присоединиться.\n'
            '2️⃣ Второе правило: НИКОГДА не забывайте о первом правиле. '
            f'Кстати вот ссылка https://t.me/{settings.bot_name}?start=rfu, чтобы рассказать всем.\n'
            f'3️⃣ Третье правило: Если ты тут, то должен выполнить задание на день.'
        )

    @pytest.mark.asyncio
    async def test_send_tasks_today(self):
        self._message.from_user.id = 12345
        self._message.answer = AsyncMock()
        self._service = RegistrationService(message=self._message)

        await self._service._send_tasks_today()

        self._message.answer.assert_called_once_with(
            '📝 Задание на первый день:\n\n'
            '1️⃣ Заполни свой профиль. Для этого нажми на кнопку "Профиль" внизу экрана.\n'
            '2️⃣ Прочитать 5 предложений.\n'
        )
