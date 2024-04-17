from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from bot import dispatcher
from choices import State
from services import LearnWordsService


@dispatcher.message_handler(Text(equals='Read'), state=State.learn_words.value)
async def handle_learn_words(message: types.Message, state: FSMContext) -> None:
    """Handle learn words."""
    await LearnWordsService(message=message, state=state).do()
