from typing import Optional

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message

from choices import State
from dto.telegram_user import TelegramUserDTOModel
from functions import create_keyboard_for_en_levels, update_data_by_api
from services.update_profile import UpdateProfileService


class WaitNameService:
    """Wait name from user."""

    _telegram_user: Optional[TelegramUserDTOModel]
    _message: Message
    _state: FSMContext
    _new_name: str
    _chat_id: int

    def __init__(self, message: Message, state: FSMContext) -> None:
        """
        Init.

        :param message: Message object.
        :param state: State object.
        """
        self._message = message
        self._state = state
        self._telegram_user = None
        self._new_name = self._message.text.title()
        self._chat_id = self._message.from_user.id

    async def do(self) -> None:
        """Wait name."""
        await self._get_user()
        await self._get_message_text()

    async def _get_user(self) -> None:
        data = await self._state.get_data()
        self._telegram_user = data['user']

    async def _get_message_text(self) -> None:
        if self._telegram_user.previous_stage == State.new_client.value:
            await self._update_name_for_new_client()
        else:
            await self._update_name_for_old_client()

    async def _update_name_for_new_client(self) -> None:

        data_for_update_user = {
            'telegram_id': self._telegram_user.telegram_id,
            'user_name': self._new_name,
            'stage': State.wait_en_level.value,
        }

        is_update_user = await update_data_by_api(
            telegram_id=self._chat_id,
            params_for_update=data_for_update_user,
            url_for_update=f'telegram_user/{self._chat_id}',
        )
        if is_update_user is False:
            return
        
        message_text = (
            f'Имя профиля изменено на {self._new_name}.\n'
            f'Выберите уровень знаний английского языка. Сейчас вам доступны 2 первых уровня, '
            f'но потом откроются новые уровни знаний.'
        )

        inline_kb = await create_keyboard_for_en_levels(hero_level=self._telegram_user.hero_level.order)

        await self._message.answer(text=message_text, reply_markup=inline_kb)

    async def _update_name_for_old_client(self) -> None:

        data_for_update_user = {
            'telegram_id': self._telegram_user.telegram_id,
            'user_name': self._new_name,
            'stage': State.update_profile.value,
        }

        is_update_user = await update_data_by_api(
            telegram_id=self._chat_id,
            params_for_update=data_for_update_user,
            url_for_update=f'telegram_user/{self._chat_id}',
        )
        if is_update_user is False:
            return

        start_message_text = '🤖 Имя обновлено.\n'

        await UpdateProfileService(chat_id=self._chat_id, start_message_text=start_message_text).do()
