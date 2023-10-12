from http import HTTPStatus
from typing import Optional

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from choices import State
from context_managers import http_client
from dto.telegram_user import TelegramUserDTOModel
from settings import settings


class WaitEnLevelService:
    """Wait en level from user."""

    _telegram_user: Optional[TelegramUserDTOModel]
    _inline_kd: InlineKeyboardMarkup
    _stage: str
    _message_text: str

    def __init__(self, callback_query: CallbackQuery, state: FSMContext):
        """Init."""
        self._callback_query = callback_query
        self._state = state
        self._telegram_user = None
        self._new_level = self._callback_query.data
        self._inline_kb = InlineKeyboardMarkup()

    async def do(self) -> None:
        """Wait en level."""
        await self._get_user()
        if self._telegram_user.previous_stage == State.new_client.value:
            state = State.read_book.value
        else:
            state = State.update_profile.value

    async def _get_user(self):
        data = await self._state.get_data()
        self._telegram_user = data['user']
