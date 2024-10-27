from typing import Union

from aiogram.types import (
    CallbackQuery,
    Message,
    ParseMode,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.dispatcher.storage import FSMContext
from loguru import logger

from bot import bot
from functions import get_data_by_api_func, get_end_of_russian_word_func, delete_message


class EndReadTodayService:
    """Service for reading sentence."""

    message: Union[CallbackQuery, Message]
    state: FSMContext
    messages_for_delete: list
    minutes_for_repeat_word: int

    def __init__(self, message: Union[CallbackQuery, Message], state: FSMContext) -> None:
        """Init."""
        self.message = message
        self.state = state
        self.minutes_for_repeat_word = 1

    async def work(self) -> None:
        logger.debug(f"message = {self.message}")
        await delete_message(message=self.message, state=self.state)
        await self._get_messages_for_delete()
        await self._send_message_end_sentences()
        await self._get_user_stats()
        if self.minutes_for_repeat_word == 0:
            await self._send_message_repeat_words()
        else:
            await self._send_message_time_to_repeat_words()

        await self.state.update_data(messages_for_delete=self.messages_for_delete)

    async def _get_messages_for_delete(self) -> None:
        data = await self.state.get_data()
        self.messages_for_delete = data.get("messages_for_delete", [])

    async def _send_message_end_sentences(self) -> None:
        message_text = "Вы прочитали все предложения на сегодня. Новые предложения будут доступны завтра."
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton(text="Read"))

        send_message = await bot.send_message(
            chat_id=self.message.from_user.id,
            text=message_text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard,
        )
        logger.debug(f"send message = {send_message.__dict__}")
        self.messages_for_delete.append(send_message.message_id)

    async def _get_user_stats(self) -> None:
        if isinstance(self.message, CallbackQuery):
            telegram_id = self.message.message.chat.id
        else:
            telegram_id = self.message.chat.id

        user_stats = await get_data_by_api_func(
            telegram_id=telegram_id, params_for_get={}, url_for_get=f"read/stats/{telegram_id}"
        )

        self.minutes_for_repeat_word = user_stats["time_to_next_word"]

    async def _send_message_repeat_words(self) -> None:
        message_with_grammar = "Но можно продолжить повторение слов"
        inline_keyboard = InlineKeyboardMarkup()
        inline_keyboard.add(InlineKeyboardButton(text="Повторение слов", callback_data="learn_words_again"))
        send_message = await bot.send_message(
            chat_id=self.message.from_user.id,
            text=message_with_grammar,
            parse_mode=ParseMode.HTML,
            reply_markup=inline_keyboard,
        )
        self.messages_for_delete.append(send_message.message_id)

    async def _send_message_time_to_repeat_words(self) -> None:
        word_minute_with_ending = get_end_of_russian_word_func(
            number=self.minutes_for_repeat_word, endings=["минуту", "минуты", "минут"]
        )
        message = (
            "Слова для повторения тоже закончились. "
            f"Новые слова для повторения появятся через {self.minutes_for_repeat_word} {word_minute_with_ending}"
        )
        send_message = await bot.send_message(
            chat_id=self.message.from_user.id,
            text=message,
            parse_mode=ParseMode.HTML,
        )
        self.messages_for_delete.append(send_message.message_id)
