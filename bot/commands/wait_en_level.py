from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message

from bot import bot, dispatcher
from choices import State
from services import WaitEnLevelService


@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith('level_en_'), state=State.wait_en_level.value)
async def handle_wait_en_level(callback_query: CallbackQuery, state: FSMContext):
    """Handle wait en level."""
    await WaitEnLevelService(callback_query=callback_query, state=state).do()


@dispatcher.message_handler(state=State.wait_en_level.value)
@dispatcher.callback_query_handler(state=State.wait_en_level.value)
async def handle_wait_en_level_incorrect_text(message: Message):
    """Handle incorrect wait en level if was text message."""
    message_text = 'Нужно нажать по одной из кнопок, чтобы изменить уровень английского.'
    await bot.send_message(chat_id=message.from_user.id, text=message_text)
