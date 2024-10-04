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
from dto import TelegramUserDTOModel
from functions import send_message_end_read_today_func, update_learn_word
from services import ReadSentenceService


@dispatcher.message_handler(Text(equals="Read"), state=State.read_book.value)
@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith("know_word_"), state=State.read_book.value)
async def handle_read_sentence(message: Union[CallbackQuery, Message], state: FSMContext) -> None:
    """Handle check words after push button read."""
    await ReadSentenceService(message=message, state=state).do()


@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith("learn_word_"), state=State.read_book.value)
async def handle_read_sentence_after_learn_words(message: Union[CallbackQuery, Message], state: FSMContext) -> None:
    """Handle read sentence after push button learn words."""
    data = await state.get_data()
    telegram_user: TelegramUserDTOModel = data["telegram_user"]
    if telegram_user.learn_words:
        first_word = telegram_user.learn_words.pop(0)
        is_update = await update_learn_word(message=message, word=first_word)
    else:
        is_update = True
    if is_update:
        await state.set_data(data={"user": telegram_user})  # Обновляем состояние без первого слова в learn_words
        return await ReadSentenceService(message=message, state=state).do()
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Что-то пошло не так, попробуй ещё раз",
    )


@dispatcher.message_handler(state=State.read_book.value)
@dispatcher.callback_query_handler(state=State.read_book.value)
async def handle_read_sentence_other_data(message: Union[CallbackQuery, Message]) -> None:
    """Handle check words after push button read."""
    message_text = "Нужно нажать по кнопке Read"
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="Read"))
    await bot.send_message(
        chat_id=message.from_user.id, text=message_text, parse_mode=ParseMode.HTML, reply_markup=keyboard
    )


@dispatcher.callback_query_handler(
    lambda c: c.data and c.data.startswith("learn_word_"), state=State.read_book_end.value
)
async def handle_end_read_sentence_today_after_learn_words(message: CallbackQuery, state: FSMContext) -> None:
    """Handle if user read all sentences today after push button learn word."""
    data = await state.get_data()
    telegram_user: TelegramUserDTOModel = data["telegram_user"]
    if telegram_user.learn_words:
        first_word = telegram_user.learn_words.pop(0)
        is_update = await update_learn_word(message=message, word=first_word)
    else:
        is_update = True
    if is_update:
        await send_message_end_read_today_func(message=message, state=state)
        return
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Что-то пошло не так, попробуй ещё раз",
    )


@dispatcher.message_handler(state=State.read_book_end.value)
@dispatcher.callback_query_handler(state=State.read_book_end.value)
async def handle_end_read_sentence_today(message: Union[CallbackQuery, Message], state: FSMContext) -> None:
    """Handle if user read all sentences today."""
    await send_message_end_read_today_func(message=message, state=state)
