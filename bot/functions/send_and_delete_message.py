from typing import Union

from asyncio import sleep as asyncio_sleep
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound

from bot import bot


async def send_message_and_delete(chat_id: int, message_text: str, reply_markup=None) -> None:
    """Function for send message and delete it."""
    send_message = await bot.send_message(chat_id=chat_id, text=message_text, reply_markup=reply_markup)
    print('send_message_and_delete', send_message, send_message.message_id, send_message.from_user)
    await delete_message(message=send_message)


async def delete_message(message: Union[CallbackQuery, Message]) -> None:
    """Function for delete message."""

    if isinstance(message, CallbackQuery):
        message_id = message.message.message_id
    else:
        message_id = message.message_id

    try:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message_id)
    except (AttributeError, MessageCantBeDeleted, MessageToDeleteNotFound):
        pass
