from typing import Union

from aiogram.types import (
    CallbackQuery,
    Message,
    ParseMode,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.dispatcher import FSMContext
from loguru import logger

from bot import bot
from choices import PartOfSpeechChoice
from dto import WordDTOModel
from functions import delete_message


async def send_message_learn_word(
    word: WordDTOModel,
    telegram_id: int,
    message: Union[CallbackQuery, Message],
    state: FSMContext,
) -> None:
    """
    Send message for learn word.

    :params word: word by WordDTOModel.
    :params telegram_id: users telegram id.
    """
    await delete_message(message=message, state=state)
    translate_word = word.translation.get("ru")
    translate_word += (60 - len(translate_word)) * " " + "."
    part_of_speech = PartOfSpeechChoice[word.part_of_speech].value

    message_text = (
        f"Помните перевод слова:\n<b><u>{word.word}</u></b> ({part_of_speech}) - {word.transcription}\n\n"
        f"Перевод: <tg-spoiler>\n{translate_word}</tg-spoiler>"
    )
    logger.debug(f"message text = {message_text}")

    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(InlineKeyboardButton(text="Помню", callback_data="learn_word_yes"))
    inline_keyboard.add(InlineKeyboardButton(text="Не помню", callback_data="learn_word_no"))
    logger.debug(f"keyboard = {inline_keyboard}")

    await bot.send_message(
        chat_id=telegram_id,
        text=message_text,
        parse_mode=ParseMode.HTML,
        reply_markup=inline_keyboard,
    )
