from typing import Union

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ParseMode,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from loguru import logger

from bot import bot
from functions.send_and_delete_message import delete_message


async def send_message_end_read_today_func(message: Union[CallbackQuery, Message], state: FSMContext) -> None:
    logger.debug(f"message = {message}")
    await delete_message(message=message, state=state)
    message_text = "Вы прочитали все предложения на сегодня. Новые предложения будут доступны завтра."
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="Read"))

    data = await state.get_data()
    messages_for_delete = data.get("messages_for_delete", [])

    send_message = await bot.send_message(
        chat_id=message.from_user.id,
        text=message_text,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )
    logger.debug(f"send message = {send_message.__dict__}")
    messages_for_delete.append(send_message.message_id)

    message_with_grammar = "Но можно продолжить повторение слов"
    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(InlineKeyboardButton(text="Повторение слов", callback_data="learn_words_again"))
    send_message = await bot.send_message(
        chat_id=message.from_user.id,
        text=message_with_grammar,
        parse_mode=ParseMode.HTML,
        reply_markup=inline_keyboard,
    )
    messages_for_delete.append(send_message.message_id)
    await state.update_data(messages_for_delete=messages_for_delete)
