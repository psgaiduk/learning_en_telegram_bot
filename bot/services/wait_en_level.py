from typing import Optional

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from bot import bot
from choices import State
from dto.telegram_user import TelegramUserDTOModel
from functions import update_data_by_api
from services.update_profile import UpdateProfileService


class WaitEnLevelService:
    """Wait en level from user."""

    _telegram_user: Optional[TelegramUserDTOModel]
    _new_level: int
    _chat_id: int

    def __init__(self, callback_query: CallbackQuery, state: FSMContext):
        """Init."""
        self._callback_query = callback_query
        self._state = state
        self._telegram_user = None
        self._new_level = int(self._callback_query.data.split('_')[-1])
        self._chat_id = self._callback_query.from_user.id

    async def do(self) -> None:
        """Wait en level."""
        await self._get_user()
        await self._get_message_text()

    async def _get_user(self) -> None:
        data = await self._state.get_data()
        self._telegram_user = data['user']

    async def _get_message_text(self) -> None:
        if self._telegram_user.previous_stage == State.new_client.value:
            await self._update_en_level_for_new_client()
        else:
            await self._update_en_level_for_old_client()

    async def _update_en_level_for_new_client(self) -> None:

        data_for_update_user = {
            'telegram_id': self._chat_id,
            'level_en_id': self._new_level,
            'stage': State.read_book.value,
            'previous_stage': '',
        }

        is_update_user = await update_data_by_api(
            telegram_id=self._chat_id,
            params_for_update=data_for_update_user,
            url_for_update=f'telegram_user/{self._chat_id}',
        )
        if is_update_user is False:
            return

        first_task_complete_text = 'Поздравляю с регистрацией! Теперь ты можешь прочитать первый рассказ. Для этого нажми по кнопке Read'
        await bot.send_message(chat_id=self._callback_query.from_user.id, text=first_task_complete_text)

    async def _update_en_level_for_old_client(self) -> None:

        data_for_update_user = {
            'telegram_id': self._telegram_user.telegram_id,
            'level_en_id': self._new_level,
            'stage': State.update_profile.value,
        }

        is_update_user = await update_data_by_api(
            telegram_id=self._chat_id,
            params_for_update=data_for_update_user,
            url_for_update=f'telegram_user/{self._chat_id}',
        )
        if is_update_user is False:
            return

        start_message_text = '🤖 Уровень английского изменён.\n'

        update_profile = UpdateProfileService(chat_id=self._chat_id, start_message_text=start_message_text)
        await update_profile.do()
