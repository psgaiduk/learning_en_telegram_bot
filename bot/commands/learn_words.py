from typing import Union

from aiogram import types
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.storage import FSMContext

from bot import bot, dispatcher
from choices import State
from services import LearnWordsService


@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith('learn_word_'), state=State.learn_words.value)
async def handle_learn_words(message: types.Message, state: FSMContext) -> None:
    """Handle learn words."""
    await LearnWordsService(message=message, state=state).do()


@dispatcher.message_handler(state=State.learn_words.value)
@dispatcher.callback_query_handler(state=State.learn_words.value)
async def handle_error_learn_words(message_data: Union[CallbackQuery, Message]) -> None:
    """Handle learn words for other data."""
    message_text = 'Нужно нажать по кнопке "Помню" или "Не помню"'
    await bot.send_message(chat_id=message_data.from_user.id, text=message_text)
