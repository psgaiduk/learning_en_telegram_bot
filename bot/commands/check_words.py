from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from bot import dispatcher
from choices import State
from functions import update_data_by_api


@dispatcher.message_handler(Text(equals='Read'), state=State.check_words.value)
async def handle_check_words_after_read(message: Message, state: FSMContext):
    """Handle check words after push button read."""
    
    start_text_message = 'Прежде чем начать изучать предложение, давай посмотрим слова, которые нам встретятся в этом предложении.'
    await message.answer(text=start_text_message)

    data = await state.get_data()
    telegram_user = data['user']
    words = telegram_user.new_sentence.words
    first_word = words.pop(0)

    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(InlineKeyboardButton(text='Знаю', callback_data=f'know_word_true_{first_word.word_id}'))
    inline_keyboard.add(InlineKeyboardButton(text='Не знаю', callback_data=f'know_word_false_{first_word.word_id}'))

    data_for_update_user = {
        'telegram_id': telegram_user.telegram_id,
        'stage': State.read_book.value,
    }

    is_update_user = await update_data_by_api(
        telegram_id=telegram_user.telegram_id,
        params_for_update=data_for_update_user,
        url_for_update=f'telegram_user/{telegram_user.telegram_id}',
    )
    if is_update_user is False:
        return

    text_message = f'Слово: {first_word.word}\nПеревод: {first_word.translation["ru"]}'
    await message.answer(text=text_message, reply_markup=inline_keyboard)
