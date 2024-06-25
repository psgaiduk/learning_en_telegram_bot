from datetime import datetime, timedelta
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
from loguru import logger

from bot import bot
from choices import EnglishLevels, State
from dto import TelegramUserDTOModel, WordDTOModel
from functions import send_message_learn_word, update_data_by_api


class LearnWordsService:
    """Service for learn words after sentence."""

    telegram_user: TelegramUserDTOModel
    state: FSMContext
    message: CallbackQuery
    first_word: WordDTOModel = None

    def __init__(self, message: CallbackQuery, state: FSMContext) -> None:
        """Init."""
        self.message = message
        self.state = state

    async def do(self) -> None:
        """Start work service."""

        await self._get_first_word()
        is_update = await self._update_learn_word()
        if not is_update:
            return await bot.send_message(
                chat_id=self.message.from_user.id,
                text='Что-то пошло не так, попробуй ещё раз',
            )

        await self._state.set_data(data={'user': self._telegram_user})  # Обновляем состояние без первого слова в learn_words
        if self.telegram_user.learn_words:
            await send_message_learn_word(word=self.telegram_user.learn_words[0], telegram_id=self.telegram_user.telegram_id)
            return

    async def _get_first_word(self) -> None:
        self.first_word = self.telegram_user.learn_words.pop(0)
        logger.debug(f'first word = {self.first_word},{self.message}')

    async def _update_learn_word(self) -> None:
        if 'yes' in self._message.data:
            self.first_word.increase_factor += 0.05
            self.first_word.interval_repeat *= 0.05
            if self.first_word.increase_factor > 2:
                self.first_word.increase_factor = 2
        else:
            self.first_word.increase_factor -= 0.1
            self.interval_repeat = 60
            if self.first_word.increase_factor < 1.1:
                self.first_word.increase_factor = 1.1

        self.first_word.repeat_datetime = datetime.now() + timedelta(seconds=self.first_word.interval_repeat)

        data_for_update_word = {
            'telegram_user_id': self.message.from_user.id,
            'word_id': self.first_word.word_id,
            'increase_factor': self.first_word.increase_factor,
            'interval_repeat': self.first_word.interval_repeat,
            'repeat_datetime': self.first_word.repeat_datetime,
        }

        logger.debug(f'data_for_update_word: {data_for_update_word}')

        is_update_history = await update_data_by_api(
            telegram_id=self.message.from_user.id,
            params_for_update=data_for_update_word,
            url_for_update='history/words',
        )

        logger.debug(f'is_update_history: {is_update_history}')
        return is_update_history
