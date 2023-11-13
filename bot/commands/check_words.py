from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from bot import bot, dispatcher
from choices import State
from functions import update_data_by_api
from services import CheckWordsService


@dispatcher.message_handler(Text(equals='Read'), state=State.check_words.value)
async def handle_check_words_after_read(message: Message, state: FSMContext):
    """Handle check words after push button read."""
    
    start_text_message = 'Прежде чем начать изучать предложение, давай посмотрим слова, которые нам встретятся в этом предложении.\n\n'

    await CheckWordsService(state=state, start_text_message=start_text_message).do()


@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith('know_word_'), state=State.check_words.value)
async def handle_check_word_click_known(callback_query: CallbackQuery, state: FSMContext):
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

    await CheckWordsService(state=state, start_text_message=start_text_message).do()

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)


@dispatcher.callback_query_handler(state=State.check_words.value)
@dispatcher.message_handler(state=State.check_words.value)
async def handle_check_words_other_data(callback_query: CallbackQuery):
    """Handle check words for other data."""
    message_text = 'Нужно нажать по кнопке Read или I know/I don\'t know'
    await bot.send_message(chat_id=callback_query.from_user.id, text=message_text)
