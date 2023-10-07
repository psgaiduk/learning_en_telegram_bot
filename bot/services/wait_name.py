from http import HTTPStatus
from typing import Optional

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from choices import State
from context_managers import http_client
from dto.telegram_user import TelegramUserDTOModel
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

    async def do(self) -> None:
        """Wait name."""
        await self._get_user()

        if self._telegram_user.previous_stage == State.new_client.value:
            await self._update_name_for_new_client()
        else:
            await self._update_name_for_old_client()

        await self._update_user()

        await self._message.answer(text=self._message_text, reply_markup=self._inline_kb)

    async def _get_user(self):
        data = await self._state.get_data()
        self._telegram_user = data['user']
        
    async def _update_name_for_new_client(self):
        self._stage = 'WAIT_EN_LEVEL'
        self._message_text = (f'Имя профиля изменено на {self._new_name}.\n'
                        f'Выберите уровень знаний английского языка. Сейчас вам доступны 2 первых уровня, '
                        f'но с увлечинием уровня, будут открываться новые уровни знаний.')
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

    async def _update_name_for_old_client(self):
        self._stage = 'UPDATE_PROFILE'
        self._inline_kb.add(InlineKeyboardButton(text='Change english level', callback_data='user_profile_change_en_level'))
        self._inline_kb.add(InlineKeyboardButton(text='Change name', callback_data='user_pofile_change_name'))
        self._inline_kb.add(InlineKeyboardButton(text='Close', callback_data='user_profile_close'))
        self._message_text = f'Имя профиля изменено на {self._new_name}.\nВыберите дальнейшее действие:'

    async def _update_user(self):
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
            self._message_text = '🤖 Что-то пошло не так. Попробуйте еще раз, чуть позже.'
            self._inline_kb = None
