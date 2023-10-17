from http import HTTPStatus
from typing import Optional

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from choices import State
from context_managers import http_client
from dto.telegram_user import TelegramUserDTOModel
from services.update_profile import UpdateProfileService
from settings import settings


class WaitNameService:
    """Wait name from user."""

    _telegram_user: Optional[TelegramUserDTOModel]
    _inline_kd: InlineKeyboardMarkup
    _stage: str
    _message_text: str

    def __init__(self, message: Message, state: FSMContext):
        """Init."""
        self._message = message
        self._state = state
        self._telegram_user = None
        self._new_name = self._message.text.title()
        self._inline_kb = InlineKeyboardMarkup()
        self._chat_id = self._message.from_user.id

    async def do(self) -> None:
        """Wait name."""
        await self._get_user()
        await self._get_message_text()

    async def _get_user(self):
        data = await self._state.get_data()
        self._telegram_user = data['user']

    async def _get_message_text(self):
        if self._telegram_user.previous_stage == State.new_client.value:
            await self._update_name_for_new_client()
        else:
            await self._update_name_for_old_client()

    async def _update_name_for_new_client(self):
        self._stage = State.wait_en_level.value
        
        is_update_user = await self._update_user()
        if is_update_user is False:
            return
        
        self._message_text = (
            f'Имя профиля изменено на {self._new_name}.\n'
            f'Выберите уровень знаний английского языка. Сейчас вам доступны 2 первых уровня, '
            f'но с увлечинием уровня, будут открываться новые уровни знаний.'
        )
        self._inline_kb.add(InlineKeyboardButton(text='A1 - Beginner', callback_data='level_en_1'))
        self._inline_kb.add(InlineKeyboardButton(text='A2 - Elementary', callback_data='level_en_2'))

        level_buttons = [
            {'hero_level': 10, 'text': 'B1 - Pre-intermediate', 'callback_data': 'level_en_3'},
            {'hero_level': 25, 'text': 'B2 - Intermediate', 'callback_data': 'level_en_4'},
            {'hero_level': 50, 'text': 'C1 - Upper-intermediate', 'callback_data': 'level_en_5'},
            {'hero_level': 80, 'text': 'C2 - Advanced', 'callback_data': 'level_en_6'},
        ]

        for button in level_buttons:
            if self._telegram_user.hero_level.order > button['hero_level']:
                self._inline_kb.add(InlineKeyboardButton(text=button['text'], callback_data=button['callback_data']))

        await self._message.answer(text=self._message_text, reply_markup=self._inline_kb)

    async def _update_name_for_old_client(self):
        self._stage = State.update_profile.value

        is_update_user = await self._update_user()
        if is_update_user is False:
            return

        self._message_text = '🤖 Имя обновлено.\n'

        await UpdateProfileService(chat_id=self._chat_id, start_message_text=self._message_text).do()

    async def _update_user(self) -> bool:

        async with http_client() as client:
            url_update_telegram_user = f'{settings.api_url}/v1/telegram_user/{self._telegram_user.telegram_id}'
            data_for_update_user = {
                'telegram_id': self._telegram_user.telegram_id,
                'user_name': self._new_name,
                'stage': self._stage,
            }
            _, response_status = await client.patch(
                url=url_update_telegram_user,
                headers=settings.api_headers,
                json=data_for_update_user,
            )

        if response_status != HTTPStatus.OK:
            message_text = '🤖 Что-то пошло не так. Попробуйте еще раз, чуть позже.'
            await self._message.answer(text=message_text)
            return False

        return True
