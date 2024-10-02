from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
from loguru import logger

from bot import bot


async def send_message_and_delete(chat_id: int, message_text: str, state: FSMContext, reply_markup=None) -> None:
    """Function for send message and delete it."""
    send_message = await bot.send_message(chat_id=chat_id, text=message_text, reply_markup=reply_markup)
    await delete_message(message=send_message, state=state)


async def delete_message(message: Union[CallbackQuery, Message], state: FSMContext) -> None:
    """Function for delete message."""

    logger.debug("delete messages")
    if isinstance(message, CallbackQuery):
        message_id = message.message.message_id
        chat_id = message.message.chat.id
    else:
        message_id = message.message_id
        chat_id = message.chat.id
    logger.debug(f"get chat_id = {chat_id} message id = {message_id}")

    state_data = await state.get_data()
    logger.debug(f"state data = {state_data}")
    messages_id_to_delete = state_data.get("messages_for_delete")
    logger.debug(f"get messages id to delete = {messages_id_to_delete}")

    if messages_id_to_delete:
        messages_id_to_delete.append(message_id)
        await state.update_data(message_to_delete=None)
    else:
        messages_id_to_delete = [message_id]
    logger.debug(f"update messages id to delete = {messages_id_to_delete}")

    for message_id_to_delete in messages_id_to_delete:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id_to_delete)
        except (AttributeError, MessageCantBeDeleted, MessageToDeleteNotFound):
            pass
