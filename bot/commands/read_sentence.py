from os import path
from random import choices, randint
from typing import Union

from aiogram.types import (
    CallbackQuery,
    Message,
    ParseMode,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from bot import bot, dispatcher
from choices import State
from dto import TelegramUserDTOModel
from functions import get_combinations, delete_message, update_data_by_api


@dispatcher.message_handler(Text(equals='Read'), state=State.read_book.value)
@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith('know_word_'), state=State.read_book.value)
async def handle_read_sentence(message: Union[CallbackQuery, Message], state: FSMContext):
    """Handle check words after push button read."""

    data = await state.get_data()
    telegram_user: TelegramUserDTOModel = data['user']

    sentence_text = telegram_user.new_sentence.text
    if telegram_user.level_en.order < 3:
        sentence_text = telegram_user.new_sentence.text_with_words

    sentence_translation = telegram_user.new_sentence.translation.get('ru')

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text='Read'))
    file_path = f'static/audio/{telegram_user.new_sentence.book_id} - {telegram_user.new_sentence.order}.mp3'

    if randint(1, 3) == 1 and path.isfile(file_path):
        with open(file_path, 'rb') as audio:

            message_text = f'Translate:\n\n<tg-spoiler>{sentence_translation}</tg-spoiler>'
            sentence_text = f'Text:\n\n<tg-spoiler>{sentence_text}</tg-spoiler>'

            await bot.send_audio(
                chat_id=telegram_user.telegram_id,
                audio=audio,
                caption=sentence_text,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard,
            )
    else:
        message_text = f'{sentence_text}\n\n<tg-spoiler>{sentence_translation}</tg-spoiler>'

    await delete_message(message=message)

    if randint(1, 6) == 1:
        await bot.send_message(chat_id=telegram_user.telegram_id, text=message_text, parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
        message_text = 'К какому времени относится предложение?'
        right_answer = telegram_user.new_sentence.sentence_times
        count_times_in_sentence = right_answer.count(',') + 1
        all_english_times = get_combinations(count_times_in_sentence)
        all_answers = [right_answer]
        other_answers = choices(all_english_times, k=3)
        all_answers.extend(other_answers)

        sorted(all_answers, key=lambda x: randint(1, 100))
        keyboard = InlineKeyboardMarkup()
        for answer in all_answers:
            callback_data = 'wrong_answer_time' if answer != right_answer else 'right_answer_time'
            keyboard.add(InlineKeyboardButton(text=answer, callback_data=callback_data))

        await bot.send_message(chat_id=telegram_user.telegram_id, text=message_text, parse_mode=ParseMode.HTML, reply_markup=keyboard)

        params_for_update_user = {
            'telegram_id': message.from_user.id,
            'stage': State.check_answer_time.value,
        }

        is_update = await update_data_by_api(
            telegram_id=message.from_user.id,
            params_for_update=params_for_update_user,
            url_for_update=f'telegram_user/{message.from_user.id}',
        )

        if is_update is False:
            return

    else:
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

        await bot.send_message(chat_id=telegram_user.telegram_id, text=message_text, parse_mode=ParseMode.HTML, reply_markup=keyboard)


@dispatcher.message_handler(state=State.read_book.value)
@dispatcher.callback_query_handler(state=State.read_book.value)
async def handle_read_sentence_other_data(message: Union[CallbackQuery, Message]):
    """Handle check words after push button read."""
    message_text = 'Нужно нажать по кнопке Read'
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text='Read'))
    await bot.send_message(chat_id=message.from_user.id, text=message_text, parse_mode=ParseMode.HTML, reply_markup=keyboard)


@dispatcher.message_handler(state=State.read_book_end.value)
@dispatcher.callback_query_handler(state=State.read_book_end.value)
async def handle_end_read_sentence_today(message: Union[CallbackQuery, Message]):
    """Handle if user read all sentences today."""

    message_text = 'Вы прочитали все предложения на сегодня. Приходите завтра.'

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text='Read'))

    await bot.send_message(chat_id=message.from_user.id, text=message_text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    await delete_message(message=message)
