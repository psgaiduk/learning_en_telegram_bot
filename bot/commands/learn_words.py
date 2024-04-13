from aiogram import types
from aiogram.dispatcher.filters import Text

from bot import bot, dispatcher
from choices import State


@dispatcher.message_handler(Text(equals='Read'), state=State.learn_words.value)
async def handle_learn_words(message: types.Message) -> None:
    """Handle learn words."""
    await bot.send_message(
        chat_id=message.from_user.id,
        text='learn words',
    )
