from typing import Union

from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import MessageCantBeDeleted

from bot import bot, dispatcher
from choices import State
from functions import send_message_and_delete, update_data_by_api
from services import CheckWordsService


@dispatcher.message_handler(Text(equals='Read'), state=State.check_words.value)
async def handle_check_words_after_read(message: Message, state: FSMContext) -> None:
    """Handle check words after push button read."""

    start_text_message = 'Прежде чем начать изучать предложение, давай посмотрим слова, которые нам встретятся в этом предложении.\n\n'
    await send_message_and_delete(chat_id=message.from_user.id, message_text=start_text_message, reply_markup=ReplyKeyboardRemove())

    await CheckWordsService(state=state, start_text_message='').do()
    
    try:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    except AttributeError:
        pass


@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith('know_word_'), state=State.check_words.value)
async def handle_check_word_click_known(callback_query: CallbackQuery, state: FSMContext) -> None:
    """Handle check word if user push button know."""
    is_known = False
    start_text_message = ''
    word_id = int(callback_query.data.split('_')[-1])
    if 'know_word_true' in callback_query.data:
        is_known = True
        start_text_message = 'Отлично! Больше мы его тебе не будем показывать. Давай продолжим.\n\n'

    data_for_update_word = {
        'telegram_user_id': callback_query.from_user.id,
        'word_id': word_id,
        'is_known': is_known,
    }

    is_update_history = await update_data_by_api(
        telegram_id=callback_query.from_user.id,
        params_for_update=data_for_update_word,
        url_for_update=f'history/words',
    )

    if is_update_history is False:
        return
    
    try:
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    except (AttributeError, MessageCantBeDeleted):
        pass

    await CheckWordsService(state=state, start_text_message=start_text_message).do()


@dispatcher.callback_query_handler(state=State.check_words.value)
@dispatcher.message_handler(state=State.check_words.value)
async def handle_check_words_other_data(message_data: Union[CallbackQuery, Message]) -> None:
    """Handle check words for other data."""
    message_text = 'Нужно нажать по кнопке I know или I don\'t know'
    await bot.send_message(chat_id=message_data.from_user.id, text=message_text)
