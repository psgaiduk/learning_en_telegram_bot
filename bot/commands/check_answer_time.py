from typing import Union

from aiogram.types import CallbackQuery, Message, ParseMode, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.storage import FSMContext

from bot import bot, dispatcher
from choices import State
from dto import TelegramUserDTOModel
from functions import delete_message, update_data_by_api


@dispatcher.callback_query_handler(lambda c: c.data and '_answer_time' in c.data, state=State.check_answer_time.value)
async def handle_check_answer_time(message: CallbackQuery, state: FSMContext):
    """Handle check answer about time of read sentence."""
    message_text = []
    data = await state.get_data()
    telegram_user: TelegramUserDTOModel = data['user']

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

    if 'right_answer_time' == message.data:
        message_text.append('Правильно.!\n\n')
    else:
        message_text.append(f'Правильный ответ: {telegram_user.new_sentence.sentence_times}\n\n')

    message_text.append(telegram_user.new_sentence.description_time)

    params_for_update_user = {
        'telegram_id': message.from_user.id,
        'stage': State.read_book.value,
    }

    is_update = await update_data_by_api(
        telegram_id=message.from_user.id,
        params_for_update=params_for_update_user,
        url_for_update=f'telegram_user/{message.from_user.id}',
    )

    if is_update is False:
        return

    await delete_message(message=message)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text='Read'))
    await bot.send_message(
        chat_id=message.from_user.id,
        text=''.join(message_text),
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )


@dispatcher.message_handler(state=State.check_answer_time.value)
@dispatcher.callback_query_handler(state=State.check_answer_time.value)
async def handle_check_answer_time_other_data(message: Union[CallbackQuery, Message]):
    """Handle check words after push button read."""
    message_text = 'Нужно нажать по кнопке со временем предложения.'
    await bot.send_message(chat_id=message.from_user.id, text=message_text, parse_mode=ParseMode.HTML)
