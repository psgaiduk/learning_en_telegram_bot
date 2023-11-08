from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from bot import dispatcher
from choices import State
from services import CheckWordsService


@dispatcher.message_handler(Text(equals='Read'), state=State.check_words.value)
async def handle_check_words_after_read(message: Message, state: FSMContext):
    """Handle check words after push button read."""
    
    start_text_message = 'Прежде чем начать изучать предложение, давай посмотрим слова, которые нам встретятся в этом предложении.\n\n'

    await CheckWordsService(state=state, start_text_message=start_text_message).do()

    