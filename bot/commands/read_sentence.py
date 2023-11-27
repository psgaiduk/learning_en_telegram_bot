from typing import Union

from aiogram.types import CallbackQuery, Message, ParseMode, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from bot import bot, dispatcher
from choices import State
from functions import delete_message, update_data_by_api


@dispatcher.message_handler(Text(equals='Read'), state=State.read_book.value)
@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith('know_word_'), state=State.read_book.value)
async def handle_read_sentence(message: Union[CallbackQuery, Message], state: FSMContext):
    """Handle check words after push button read."""

    data = await state.get_data()
    telegram_user = data['user']

    sentence_text = telegram_user.new_sentence.text
    sentence_translation = telegram_user.new_sentence.translation.get('ru')

    message_text = f'{sentence_text}\n\n<tg-spoiler>{sentence_translation}</tg-spoiler>'

    data_for_update_history_sentence = {
        'id': telegram_user.new_sentence.history_sentence_id,
        'is_read': True,
    }

    is_update_sentence = await update_data_by_api(
        telegram_id=telegram_user.telegram_id,
        params_for_update=data_for_update_history_sentence,
        url_for_update=f'history/sentences/{telegram_user.new_sentence.history_sentence_id}',
    )

    if is_update_sentence is False:
        return

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text='Read'))

    await bot.send_message(chat_id=telegram_user.telegram_id, text=message_text, parse_mode=ParseMode.HTML, reply_markup=keyboard)

    await delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)


@dispatcher.message_handler(state=State.read_book.value)
@dispatcher.callback_query_handler(state=State.read_book.value)
async def handle_read_sentence_other_data(message: Union[CallbackQuery, Message], state: FSMContext):
    """Handle check words after push button read."""
    message_text = 'Нужно нажать по кнопке Read'
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text='Read'))
    await bot.send_message(chat_id=message.from_user.id, text=message_text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
