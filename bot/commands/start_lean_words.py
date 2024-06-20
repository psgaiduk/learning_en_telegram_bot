from typing import Union

from aiogram.types import (
    CallbackQuery,
    Message,
    ParseMode,
    InlineKeyboardMarkup,
    InlineKeyboardButton

)
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from loguru import logger

from bot import bot, dispatcher
from dto import TelegramUserDTOModel
from choices import State
from functions import update_data_by_api


@dispatcher.message_handler(Text(equals='Read'), state=State.start_learn_words.value)
async def handle_start_lean_words(message: Message, state: FSMContext) -> None:
    """Handle start learn words after push button read."""

    data = await state.get_data()
    telegram_user: TelegramUserDTOModel = data['user']
    logger.debug(f'get telegram user = {telegram_user}')

    params_for_update_user = {
        'telegram_id': message.from_user.id,
        'stage': State.learn_words.value,
    }
    logger.debug(f'params for update user = {params_for_update_user}')

    is_update = await update_data_by_api(
        telegram_id=message.from_user.id,
        params_for_update=params_for_update_user,
        url_for_update=f'telegram_user/{message.from_user.id}',
    )
    logger.debug(f'update user = {is_update}')
    inline_keyboard = None
    message_text = '🤖 Что-то пошло не так. Попробуйте еще раз, чуть позже.'

    if is_update:
        logger.debug('Всё хорошо, можно отправлять сообщения')
        message_start_learn_word = 'Прежде чем продолжить повторим слова.'

        await bot.send_message(
            chat_id=telegram_user.telegram_id,
            text=message_start_learn_word,
            parse_mode=ParseMode.HTML,
        )

        first_word = telegram_user.learn_words[0]
        logger.debug(f'Получили первое слово = {first_word}')
        message_text = (
            f'Помните перевод слова: {first_word.word}\n'
            f'Перевод: <tg-spoiler>{first_word.translation}</tg-spoiler>'
        )
        inline_keyboard = InlineKeyboardMarkup()
        inline_keyboard.add(InlineKeyboardButton(text='I remember', callback_data='learn_word_yes'))
        inline_keyboard.add(InlineKeyboardButton(text='I don\'t remember', callback_data='learn_word_no'))

    await bot.send_message(
        chat_id=telegram_user.telegram_id,
        text=message_text,
        parse_mode=ParseMode.HTML,
        reply_markup=inline_keyboard,
    )


@dispatcher.message_handler(state=State.start_learn_words.value)
@dispatcher.callback_query_handler(state=State.start_learn_words.value)
async def handle_error_start_learn_words(message_data: Union[CallbackQuery, Message]) -> None:
    """Handle start learn words for other data."""
    message_text = 'Нужно нажать по кнопке I remember или I don\'t remember'
    await bot.send_message(chat_id=message_data.from_user.id, text=message_text)
