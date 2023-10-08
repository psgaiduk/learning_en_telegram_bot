from http import HTTPStatus

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import ClientResponse
from pytest import mark
from unittest.mock import AsyncMock, Mock, patch

from choices import State
from dto import HeroLevelDTOModel, TelegramUserDTOModel
from settings import settings
from services import WaitNameService


class TestWaitNameService:
    """Tests for RegistrationService."""

    @classmethod
    def setup_class(cls):
        cls._message = Mock()
        cls._post_method_target = 'context_managers.aio_http_client.AsyncHttpClient.post'
        cls._state = Mock()

    @mark.asyncio
    async def test_get_user(self, mocker):
        self._message.answer = AsyncMock()

        telegram_user_model = TelegramUserDTOModel(
            telegram_id=12345,
            user_name='UserName',
            experience=10,
            previous_stage='PreviousStage',
            stage='CurrentStage',
            main_language=None,
            level_en=None,
            hero_level=None,
        )
        self._state.get_data = AsyncMock(return_value={'user': telegram_user_model})

        self._service = WaitNameService(message=self._message, state=self._state)

        await self._service._get_user()
        assert self._service._telegram_user == telegram_user_model
        self._state.get_data.assert_awaited_once()

    @mark.parametrize('hero_level_order, buttons_count', [
        (0, 2), (10, 2), (11, 3), (25, 3), (26, 4), (30, 4), (50, 4), (51, 5), (60, 5), (80, 5), (81, 6), (90, 6),
    ])
    @mark.asyncio
    async def test_update_name_for_new_client(self, hero_level_order, buttons_count):
        self._message.text = 'NewName'
        self._message.answer = AsyncMock()

        hero_level = HeroLevelDTOModel(
            id=1,
            title='Level',
            order=hero_level_order,
            need_experience=0,
            count_sentences=0,
            count_games=0,
        )

        telegram_user_model = TelegramUserDTOModel(
            telegram_id=12345,
            user_name='UserName',
            experience=10,
            previous_stage='PreviousStage',
            stage='CurrentStage',
            main_language=None,
            level_en=None,
            hero_level=hero_level,
        )

        self._state.get_data = AsyncMock(return_value={'user': telegram_user_model})

        self._service = WaitNameService(message=self._message, state=self._state)
        self._service._telegram_user = telegram_user_model

        await self._service._update_name_for_new_client()

        assert self._service._stage == State.wait_name.value
        message_text = (
            'Имя профиля изменено на Newname.\n'
            'Выберите уровень знаний английского языка. Сейчас вам доступны 2 первых уровня, но с увлечинием уровня, '
            'будут открываться новые уровни знаний.'
        )
        assert message_text == self._service._message_text

        expected_buttons = [
            [InlineKeyboardButton(text='A1 - Beginner', callback_data='level_en_1')],
            [InlineKeyboardButton(text='A2 - Elementary', callback_data='level_en_2')],
            [InlineKeyboardButton(text='B1 - Pre-intermediate', callback_data='level_en_3')],
            [InlineKeyboardButton(text='B2 - Intermediate', callback_data='level_en_4')],
            [InlineKeyboardButton(text='C1 - Upper-intermediate', callback_data='level_en_5')],
            [InlineKeyboardButton(text='C2 - Advanced', callback_data='level_en_6')],
        ]

        assert self._service._inline_kb.inline_keyboard == expected_buttons[:buttons_count]

