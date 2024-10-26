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
from functions import delete_message


class EndReadTodayService:
    """Service for reading sentence."""

    message: Union[CallbackQuery, Message]
    state: FSMContext
    messages_for_delete: list

    def __init__(self, message: Union[CallbackQuery, Message], state: FSMContext) -> None:
        """Init."""
        self.message = message
        self.state = state

    async def work(self) -> None:
        logger.debug(f"message = {self.message}")
        await delete_message(message=self.message, state=self.state)
        await self._get_messages_for_delete()
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
        await self.state.update_data(messages_for_delete=self.messages_for_delete)

    async def _get_messages_for_delete(self) -> None:
        data = await self.state.get_data()
        self.messages_for_delete = data.get("messages_for_delete", [])
