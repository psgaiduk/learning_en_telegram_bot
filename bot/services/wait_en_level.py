from http import HTTPStatus
from typing import Optional, Union

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from bot import bot
from choices import State
from context_managers import http_client
from dto.telegram_user import TelegramUserDTOModel
from settings import settings


class WaitEnLevelService:
    """Wait en level from user."""

    _telegram_user: Optional[TelegramUserDTOModel]
    _stage: str
    _new_level: int
    _keyboard: Optional[Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]]
    _message_text: str

    def __init__(self, callback_query: CallbackQuery, state: FSMContext):
        """Init."""
        self._callback_query = callback_query
        self._state = state
        self._telegram_user = None
        self._keyboard = None
        self._new_level = int(self._callback_query.data.split('_')[-1])

    async def do(self) -> None:
        """Wait en level."""
        await self._get_user()
        await self._get_message_text()
        await self._update_user()
        await bot.send_message(chat_id=self._callback_query.from_user.id, text=self._message_text, reply_markup=self._keyboard)

    async def _get_user(self):
        data = await self._state.get_data()
        self._telegram_user = data['user']

    async def _get_message_text(self):
        if self._telegram_user.previous_stage == State.new_client.value:
            await self._update_en_level_for_new_client()
        else:
            await self._update_en_level_for_old_client()

    async def _update_en_level_for_new_client(self):
        self._stage = State.read_book.value
        first_task_complete_text = 'Подздравляю ты выполнил первое задание на день! Теперь ты можешь прочитать первый рассказ.'
        await bot.send_message(chat_id=self._callback_query.from_user.id, text=first_task_complete_text)
        self._message_text = 'Теперь ты готов к изучению английского языка. Для начала прочитай первый рассказ.'
        self._keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='Read'))

    async def _update_en_level_for_old_client(self):
        self._stage = State.update_profile.value
        self._message_text = 'Уровень английского языка изменен.'
        self._stage = State.update_profile.value
        self._keyboard = InlineKeyboardMarkup()
        self._keyboard.add(InlineKeyboardButton(text='Change english level', callback_data='user_profile_change_en_level'))
        self._keyboard.add(InlineKeyboardButton(text='Change name', callback_data='user_pofile_change_name'))
        self._keyboard.add(InlineKeyboardButton(text='Close', callback_data='user_profile_close'))

    async def _update_user(self):
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
            self._message_text = '🤖 Что-то пошло не так. Попробуйте еще раз, чуть позже.'
            self._keyboard = None
