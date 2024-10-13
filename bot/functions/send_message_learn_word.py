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
from choices import PartOfSpeechChoice, State
from dto import WordDTOModel
from functions import delete_message
from functions.update_data_by_api import update_data_by_api


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
    part_of_speech = PartOfSpeechChoice[word.part_of_speech].value

    message_text = (
        f"{'=' * 35}\n\n"
        f"<b><u>{word.word}</u></b> - {word.transcription}\n\n"
        f"<i>{part_of_speech}</i>\n\n"
        f"{'=' * 35}"
    )
    logger.debug(f"message text = {message_text}")

    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(InlineKeyboardButton(text="Проверить", callback_data="show_word"))
    logger.debug(f"keyboard = {inline_keyboard}")

    params_for_update_user = {
        "telegram_id": telegram_id,
        "stage": State.show_word.value,
    }

    is_update_user = await update_data_by_api(
        telegram_id=telegram_id,
        params_for_update=params_for_update_user,
        url_for_update=f"telegram_user/{telegram_id}",
    )

    if is_update_user is False:
        return

    await bot.send_message(
        chat_id=telegram_id,
        text=message_text,
        parse_mode=ParseMode.HTML,
        reply_markup=inline_keyboard,
    )
