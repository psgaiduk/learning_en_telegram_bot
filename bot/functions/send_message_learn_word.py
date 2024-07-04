from typing import Union

from aiogram.types import (
    CallbackQuery,
    Message,
    ParseMode,
    InlineKeyboardMarkup,
    InlineKeyboardButton

)
from loguru import logger

from bot import bot
from dto import WordDTOModel
from functions import delete_message


async def send_message_learn_word(word: WordDTOModel, telegram_id: int, message: Union[CallbackQuery, Message]) -> None:
    """
    Send message for learn word.

    :params word: word by WordDTOModel.
    :params telegram_id: users telegram id.
    """
    await delete_message(message=message)
    translate_word = word.translation.get("ru")
    translate_word += (30 - len(translate_word)) * ' ' + '.'

    message_text = (
        f'Помните перевод слова: <b><u>{word.word}</u></b>\n\n'
        f'Перевод: <tg-spoiler>{translate_word}</tg-spoiler>'
    )
    logger.debug(f'message text = {message_text}')

    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(InlineKeyboardButton(text='I remember', callback_data='learn_word_yes'))
    inline_keyboard.add(InlineKeyboardButton(text='I don\'t remember', callback_data='learn_word_no'))
    logger.debug(f'keyboard = {inline_keyboard}')

    await bot.send_message(
        chat_id=telegram_id,
        text=message_text,
        parse_mode=ParseMode.HTML,
        reply_markup=inline_keyboard,
    )
