from http import HTTPStatus
from typing import Optional

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from bot import bot
from choices import State
from context_managers import http_client
from dto.telegram_user import TelegramUserDTOModel
from services.update_profile import UpdateProfileService
from settings import settings


class WaitEnLevelService:
    """Wait en level from user."""

    _telegram_user: Optional[TelegramUserDTOModel]
    _stage: str
    _new_level: int

    def __init__(self, callback_query: CallbackQuery, state: FSMContext):
        """Init."""
        self._callback_query = callback_query
        self._state = state
        self._telegram_user = None
        self._new_level = int(self._callback_query.data.split('_')[-1])

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
        self._stage = State.read_book.value

        is_update_user = await self._update_user()
        if not is_update_user:
            return

        first_task_complete_text = 'Поздравляю ты выполнил первое задание на день! Теперь ты можешь прочитать первый рассказ.'
        await bot.send_message(chat_id=self._callback_query.from_user.id, text=first_task_complete_text)
        message_text = 'Теперь ты готов к изучению английского языка. Для начала прочитай первый рассказ.'
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='Read'))
        await bot.send_message(chat_id=self._callback_query.from_user.id, text=message_text, reply_markup=keyboard)

    async def _update_en_level_for_old_client(self) -> None:
        self._stage = State.update_profile.value
        
        is_update_user = await self._update_user()
        if not is_update_user:
            return

        await UpdateProfileService(chat_id=self._callback_query.from_user.id, start_message_text='🤖 Уровень английского изменён.\n').do()

    async def _update_user(self) -> bool:
        async with http_client() as client:
            url_update_telegram_user = f'{settings.api_url}/v1/telegram_user/{self._telegram_user.telegram_id}'
            data_for_update_user = {
                'telegram_id': self._telegram_user.telegram_id,
                'level_en_id': self._new_level,
                # 'stage': self._stage,
            }
            _, response_status = await client.patch(
                url=url_update_telegram_user,
                headers=settings.api_headers,
                json=data_for_update_user,
            )

        if response_status != HTTPStatus.OK:
            message_text = '🤖 Что-то пошло не так. Попробуйте еще раз, чуть позже.'
            await bot.send_message(chat_id=self._callback_query.from_user.id, text=message_text)
            return False

        return True
