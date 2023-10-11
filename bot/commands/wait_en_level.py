from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message, ContentType

from bot import bot, dispatcher
from choices import State


@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith('level_en_'), state=State.wait_en_level.value)
async def handle_wait_en_level(callback_query: CallbackQuery, state: FSMContext):
    """Handle wait en level."""
    await callback_query.answer('Уровень английского изменен.')


@dispatcher.callback_query_handler(state=State.wait_en_level.value)
async def handle_wait_en_level_incorrect_work(callback_query: CallbackQuery):
    """Handle incorrect wait en level."""
    await callback_query.answer('Нужно нажать по одной из кнопок, чтобы изменить уровень английского.')


@dispatcher.message_handler(state=State.wait_en_level.value, content_types=ContentType.TEXT)
async def handle_wait_en_level_incorrect_text_message(message: Message, state: FSMContext):
    """Handle incorrect wait en level if was text message."""
    await message.answer('Нужно нажать по одной из кнопок, чтобы изменить уровень английского.')
