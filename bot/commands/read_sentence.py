from typing import Union

from aiogram.types import (
    CallbackQuery,
    Message,
    ParseMode,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from bot import bot, dispatcher
from choices import State
from functions import delete_message
from services import ReadSentenceService


@dispatcher.message_handler(Text(equals='Read'), state=State.read_book.value)
@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith('know_word_'), state=State.read_book.value)
async def handle_read_sentence(message: Union[CallbackQuery, Message], state: FSMContext) -> None:
    """Handle check words after push button read."""
    await ReadSentenceService(message=message, state=state).do()


@dispatcher.message_handler(state=State.read_book.value)
@dispatcher.callback_query_handler(state=State.read_book.value)
async def handle_read_sentence_other_data(message: Union[CallbackQuery, Message]) -> None:
    """Handle check words after push button read."""
    message_text = 'Нужно нажать по кнопке Read'
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text='Read'))
    await bot.send_message(chat_id=message.from_user.id, text=message_text, parse_mode=ParseMode.HTML, reply_markup=keyboard)


@dispatcher.message_handler(state=State.read_book_end.value)
@dispatcher.callback_query_handler(state=State.read_book_end.value)
async def handle_end_read_sentence_today(message: Union[CallbackQuery, Message]) -> None:
    """Handle if user read all sentences today."""

    message_text = 'Вы прочитали все предложения на сегодня. Приходите завтра.'

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text='Read'))

    await bot.send_message(chat_id=message.from_user.id, text=message_text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    await delete_message(message=message)
