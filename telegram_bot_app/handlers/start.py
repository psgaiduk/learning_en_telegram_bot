from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from db.functions.users import get_user_by_telegram_id, create_user
from db.functions.texts import get_text_for_user
from telegram_bot_app.core import dispatcher


@dispatcher.message_handler(commands='start')
async def cmd_start(message: types.Message, state: FSMContext):
    """Work with command start."""
    chat_id = message.from_id
    logger.configure(extra={'chat_id': chat_id, 'work_id': datetime.now().timestamp()})
    logger.debug(f'message = {message}')

    user = await get_user_by_telegram_id(telegram_id=chat_id)
    logger.debug(f'Get user = {user}')
    if not user:
        logger.debug(f'We don\'t have this user, create new user.')
        user = await create_user(telegram_id=chat_id, name=message.from_user.first_name)
        logger.debug(f'New user = {user}')

    text, text_id = await get_text_for_user(telegram_id=user.telegram_id)
    logger.debug(f'Get new text text_id = {text_id}\n{text}')

    sentences_with_translate = text.split(']')
    logger.debug(f'Split sentences\n{sentences_with_translate}')
    sentences_for_user = []
    for sentence in sentences_with_translate:
        if '[' not in sentence:
            continue
        sentence_on_en, sentence_on_ru = sentence.strip().split('[')
        sentences_for_user.append((sentence_on_en.strip(), sentence_on_ru.strip()))

    logger.debug(f'List sentences and translate:\n{sentences_for_user}')

    current_sentence = sentences_for_user.pop(0)
    previous_sentences = [current_sentence]
    next_sentences = sentences_for_user

    logger.debug(f'current sentence\n{current_sentence}')

    await state.set_data({'previous_sentences': previous_sentences, 'next_sentences': next_sentences})

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Далее')

    text_for_user = '\n'.join(
        [
            current_sentence[0],
            '\n<u>Посмотреть перевод:</u>',
            f'<tg-spoiler>{current_sentence[1]}</tg-spoiler>'
        ])

    await message.answer(text_for_user, reply_markup=markup, parse_mode="HTML")
