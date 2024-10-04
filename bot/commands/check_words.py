from typing import Union

from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from loguru import logger

from bot import bot, dispatcher
from choices import State
from dto import TelegramUserDTOModel
from functions import delete_message, send_message_and_delete, save_word_history, update_learn_word
from services import CheckWordsService


@dispatcher.message_handler(Text(equals='Read'), state=State.check_words.value)
async def handle_check_words_after_read(message: Message, state: FSMContext) -> None:
    """Handle check words after push button read."""

    start_text_message = 'Прежде чем начать изучать предложение, давай посмотрим слова, которые нам встретятся в этом предложении.\n\n'
    await send_message_and_delete(chat_id=message.from_user.id, message_text=start_text_message, state=state, reply_markup=ReplyKeyboardRemove())

    await CheckWordsService(state=state, start_text_message='').do()

    await delete_message(message=message, state=state)


@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith('learn_word_'), state=State.check_words.value)
async def handle_check_words_after_learn_words(message: CallbackQuery, state: FSMContext) -> None:
    """Handle check answer about time of learn words."""
    data = await state.get_data()
    telegram_user: TelegramUserDTOModel = data['telegram_user']
    if telegram_user.learn_words:
        first_word = telegram_user.learn_words.pop(0)
        is_update = await update_learn_word(message=message, word=first_word)
    else:
        is_update = True
    if is_update:
        await state.update_data(telegram_user=telegram_user)  # Обновляем состояние без первого слова в learn_words
        await CheckWordsService(state=state, start_text_message='').do()
        return await delete_message(message=message, state=state)
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Что-то пошло не так, попробуй ещё раз',
    )


@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith('know_word_'), state=State.check_words.value)
async def handle_check_word_click_known(callback_query: CallbackQuery, state: FSMContext) -> None:
    """Handle check word if user push button know."""

    is_update_history, start_text_message = await save_word_history(callback_query=callback_query)

    if is_update_history is False:
        return

    await delete_message(message=callback_query, state=state)

    await CheckWordsService(state=state, start_text_message=start_text_message).do()


@dispatcher.callback_query_handler(state=State.check_words.value)
@dispatcher.message_handler(state=State.check_words.value)
async def handle_check_words_other_data(message_data: Union[CallbackQuery, Message]) -> None:
    """Handle check words for other data."""
    message_text = 'Нужно нажать по кнопке "Знаю" это слово или "Не знаю"'

    await bot.send_message(chat_id=message_data.from_user.id, text=message_text)
