from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from bot import dispatcher
from choices import State
from services import LearnWordsService


@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith('learn_word_'), state=State.learn_words.value)
async def handle_learn_words(message: types.Message, state: FSMContext) -> None:
    """Handle learn words."""
    await LearnWordsService(message=message, state=state).do()
