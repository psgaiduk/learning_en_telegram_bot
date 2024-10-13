from typing import Union

from aiogram.types import CallbackQuery, Message
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.storage import FSMContext
from loguru import logger

from bot import bot, dispatcher
from choices import State
from dto import TelegramUserDTOModel
from functions import update_data_by_api


@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith("show_word"), state=State.show_word.value)
async def handle_show_word(callback_query: CallbackQuery, state: FSMContext) -> None:
    """Handle show word."""
    data = await state.get_data()
    telegram_user: TelegramUserDTOModel = data["telegram_user"]
    word = telegram_user.learn_words[0]
    translate_word = word.translation.get("ru")
    telegram_id = callback_query.message.chat.id
    logger.debug(f"telegram_id = {telegram_id}\ncallback = {callback_query}")

    message_text = f"{'=' * 40}\n\n" f"{word.word}\n\n" f"<b><u>{translate_word}</u></b>\n\n" f"{'=' * 40}\n"
    logger.debug(f"message text = {message_text}")

    params_for_update_user = {
        "telegram_id": telegram_id,
        "stage": State.learn_words.value,
    }

    is_update_user = await update_data_by_api(
        telegram_id=telegram_id,
        params_for_update=params_for_update_user,
        url_for_update=f"telegram_user/{telegram_id}",
    )

    if is_update_user is False:
        return

    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(InlineKeyboardButton(text="Помню", callback_data="learn_word_yes"))
    inline_keyboard.add(InlineKeyboardButton(text="Не помню", callback_data="learn_word_no"))
    logger.debug(f"keyboard = {inline_keyboard}")

    await bot.edit_message_text(
        chat_id=telegram_id,
        message_id=callback_query.message.message_id,
        text=message_text,
        parse_mode=ParseMode.HTML,
        reply_markup=inline_keyboard,
    )


@dispatcher.callback_query_handler(state=State.show_word.value)
@dispatcher.message_handler(state=State.show_word.value)
async def handle_show_word_other_data(message_data: Union[CallbackQuery, Message]) -> None:
    """Handle show word for other data."""
    message_text = 'Нужно нажать по кнопке "Проверить"'

    await bot.send_message(chat_id=message_data.from_user.id, text=message_text)
