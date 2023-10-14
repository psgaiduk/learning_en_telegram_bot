from http import HTTPStatus

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytest import mark
from unittest.mock import AsyncMock, Mock, patch

from choices import State
from dto import HeroLevelDTOModel, TelegramUserDTOModel
from settings import settings
from services import WaitEnLevelService


class TestWaitEnLevelService:
    """Tests for wait en level"""

    @classmethod
    def setup_class(cls):
        cls._callback = Mock()
        cls._post_method_target = 'context_managers.aio_http_client.AsyncHttpClient.post'
        cls._state = Mock()


    @mark.asyncio
    async def test_get_user(self, mocker):
        """Test get user."""

        self._callback.from_user.id = 12345
        self._callback.data = 'level_en_1'

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

        self._service = WaitEnLevelService(callback_query=self._callback, state=self._state)

        await self._service._get_user()
        assert self._service._telegram_user == telegram_user_model
        self._state.get_data.assert_awaited_once()

    @mark.asyncio
    async def test_get_message_text_new_client(self):
        self._callback.data = 'level_en_1'
        self._service = WaitEnLevelService(callback_query=self._callback, state=self._state)
        self._service._update_en_level_for_new_client = AsyncMock()
        self._service._update_en_level_for_old_client = AsyncMock()

        self._service._telegram_user = TelegramUserDTOModel(
            telegram_id=12345,
            user_name='UserName',
            experience=10,
            previous_stage=State.new_client.value,
            stage='CurrentStage',
            main_language=None,
            level_en=None,
            hero_level=None,
        )

        await self._service._get_message_text()

        self._service._update_en_level_for_new_client.assert_called_once()
        self._service._update_en_level_for_old_client.assert_not_called()

    @mark.asyncio
    async def test_get_message_text_old_client(self):
        self._callback.data = 'level_en_1'
        self._service = WaitEnLevelService(callback_query=self._callback, state=self._state)
        self._service._update_en_level_for_new_client = AsyncMock()
        self._service._update_en_level_for_old_client = AsyncMock()

        self._service._telegram_user = TelegramUserDTOModel(
            telegram_id=12345,
            user_name='UserName',
            experience=10,
            previous_stage='',
            stage='CurrentStage',
            main_language=None,
            level_en=None,
            hero_level=None,
        )

        await self._service._get_message_text()

        self._service._update_en_level_for_new_client.assert_not_called()
        self._service._update_en_level_for_old_client.assert_called_once()
