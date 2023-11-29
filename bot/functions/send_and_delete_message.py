from aiogram.utils.exceptions import MessageCantBeDeleted

from bot import bot


async def send_message_and_delete(chat_id: int, message_text: str, reply_markup=None) -> None:
    """Function for send message and delete it."""
    send_message = await bot.send_message(chat_id=chat_id, text=message_text, reply_markup=reply_markup)
    await delete_message(chat_id=chat_id, message_id=send_message.message_id)


async def delete_message(chat_id: int, message_id: int) -> None:
    """Function for delete message."""
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except (AttributeError, MessageCantBeDeleted):
        pass
