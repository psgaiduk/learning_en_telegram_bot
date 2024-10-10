from typing import Union

from aiogram.types import (
    CallbackQuery,
    Message,
    ParseMode,
)
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from loguru import logger

from bot import bot, dispatcher
from dto import TelegramUserDTOModel
from choices import State
from functions import send_message_learn_word, update_data_by_api


@dispatcher.callback_query_handler(
    lambda c: c.data and c.data.startswith("learn_words_again"),
    state=State.start_learn_words.value,
)
@dispatcher.message_handler(Text(equals="Read"), state=State.start_learn_words.value)
async def handle_start_lean_words(message: Message, state: FSMContext) -> None:
    """Handle start learn words after push button read."""

    data = await state.get_data()
    telegram_user: TelegramUserDTOModel = data["telegram_user"]
    logger.debug(f"get telegram user = {telegram_user}")

    params_for_update_user = {
        "telegram_id": message.from_user.id,
        "stage": State.learn_words.value,
    }
    logger.debug(f"params for update user = {params_for_update_user}")

    is_update = await update_data_by_api(
        telegram_id=message.from_user.id,
        params_for_update=params_for_update_user,
        url_for_update=f"telegram_user/{message.from_user.id}",
    )
    logger.debug(f"update user = {is_update}")
    if is_update:
        logger.debug("Всё хорошо, можно отправлять сообщения")
        if isinstance(message, Message):
            message_start_learn_word = "Прежде чем продолжить повторим слова."
        else:
            message_start_learn_word = "Повторим слова"

        data = await state.get_data()
        messages_for_delete = data.get("messages_for_delete", [])

        send_message = await bot.send_message(
            chat_id=telegram_user.telegram_id,
            text=message_start_learn_word,
            parse_mode=ParseMode.HTML,
        )

        logger.debug(f"send message = {send_message.__dict__}")
        messages_for_delete.append(send_message.message_id)
        await state.update_data(messages_for_delete=messages_for_delete)

        first_word = telegram_user.learn_words[0]
        logger.debug(f"Получили первое слово = {first_word}")
        return await send_message_learn_word(
            word=first_word,
            telegram_id=telegram_user.telegram_id,
            message=message,
            state=state,
        )

    message_text = "🤖 Что-то пошло не так. Попробуйте еще раз, чуть позже."
    await bot.send_message(
        chat_id=telegram_user.telegram_id,
        text=message_text,
        parse_mode=ParseMode.HTML,
    )


@dispatcher.message_handler(state=State.start_learn_words.value)
@dispatcher.callback_query_handler(state=State.start_learn_words.value)
async def handle_error_start_learn_words(message_data: Union[CallbackQuery, Message]) -> None:
    """Handle start learn words for other data."""
    message_text = 'Нужно нажать по кнопке "Помню" или "Не помню"'
    await bot.send_message(chat_id=message_data.from_user.id, text=message_text)
