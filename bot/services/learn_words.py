from os import path
from random import choices, randint
from typing import Union

from aiogram.types import (
    CallbackQuery,
    Message,
    ParseMode,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.dispatcher.storage import FSMContext

from bot import bot
from choices import EnglishLevels, State
from dto import TelegramUserDTOModel


class LearnWordsService:
    """Service for learn words after sentence."""

    _telegram_user: TelegramUserDTOModel
    _state: FSMContext
    _message: Union[CallbackQuery, Message]

    def __init__(self, message: Union[CallbackQuery, Message], state: FSMContext) -> None:
        """Init."""
        self._message = message
        self._state = state

    async def do(self) -> None:
        """Start work service."""
        await bot.send_message(
            chat_id=self._message.from_user.id,
            text='learn words',
        )
