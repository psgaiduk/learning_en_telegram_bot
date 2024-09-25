from typing import Union

from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ParseMode,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from bot import bot
from functions.send_and_delete_message import delete_message


async def send_message_end_read_today_func(message: Union[CallbackQuery, Message]) -> None:
    message_text = "Вы прочитали все предложения на сегодня. Новые предложения будут доступны завтра."
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="Read"))

    await bot.send_message(
        chat_id=message.from_user.id, text=message_text, parse_mode=ParseMode.HTML, reply_markup=keyboard
    )
    await delete_message(message=message)
    message_with_grammar = "Но можно продолжить повторение слов"
    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(InlineKeyboardButton(text="Повторение слов", callback_data="learn_words_again"))
    await bot.send_message(
        chat_id=message.from_user.id,
        text=message_with_grammar,
        parse_mode=ParseMode.HTML,
        reply_markup=inline_keyboard,
    )
