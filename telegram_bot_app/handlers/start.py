from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger
from nltk.tokenize import sent_tokenize

from db.models import Users
from db.functions.current_text_user import (
    create_current_text_user,
    get_current_text_for_user,
    update_current_text_user,
)
from db.functions.texts import delete_text, get_text_for_user
from db.functions.texts_users import get_today_text_by_telegram_id
from telegram_bot_app.core import dispatcher
from aiogram.dispatcher.filters import Text
from telegram_bot_app.functions import (
    create_new_user,
    create_sentences_for_user,
    get_user_by_chat_id,
    create_text_for_user,
)
from telegram_bot_app.states import TextStates


languages = {'ru': 'russian', 'en': 'english', 'fr': 'french', 'es': 'spanish', 'ge': 'german'}


@dispatcher.message_handler(commands='start')
@dispatcher.message_handler(Text(equals='start', ignore_case=True))
async def cmd_start(message: types.Message, state: FSMContext):
    """Work with command start."""
    chat_id = message.from_id
    logger.configure(extra={'chat_id': chat_id, 'work_id': datetime.now().timestamp()})
    logger.debug(f'message = {message}')

    user = await get_user_by_chat_id(chat_id=chat_id)

    if not user:
        await create_new_user(chat_id=chat_id, name=message.from_user.first_name, message=message)
        return

    is_complete_text_today = await get_today_text_by_telegram_id(telegram_id=user.telegram_id)
    logger.debug(f'check have user text today = {is_complete_text_today}')
    if is_complete_text_today:
        logger.debug(f'user today have text, send about this')
        await message.answer('Вы сегодня уже прочитали текст, завтра будет новый.', parse_mode='HTML')
        return

    current_text = await get_current_text_for_user(telegram_id=user.telegram_id)

    if current_text:
        current_sentence = current_text.next_sentences.pop(0)
        previous_sentences = current_text.previous_sentences
        next_sentences = current_text.next_sentences
        text_id = current_text.text_id
        logger.debug(f'text id = {text_id}\n'
                     f'previous sentences = {previous_sentences}\n'
                     f'nex sentences = {next_sentences}')

        message_for_user = 'Что-то пошло не так, но мы продолжаем.'
        await message.answer(message_for_user, parse_mode='HTML')

    else:
        sentences, translate_sentences, text_id = await get_texts(user=user)
        sentences_for_user = await create_sentences_for_user(
            sentences=sentences,
            translate_sentences=translate_sentences,
            user=user,
        )
        logger.debug(f'List sentences and translate:\n{sentences_for_user}')

        current_sentence = sentences_for_user.pop(0)
        previous_sentences = [current_sentence]
        next_sentences = sentences_for_user

    await state.set_data(
        {
            'previous_sentences': previous_sentences,
            'next_sentences': next_sentences,
            'user': user,
            'text_id': text_id,
        }
    )

    logger.debug(f'current sentence\n{current_sentence}')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Далее')

    text_for_user = create_text_for_user(current_sentence=current_sentence, next_sentences=next_sentences)

    await TextStates.next_sentence.set()

    if current_text:
        await update_current_text_user(
            telegram_id=user.telegram_id,
            next_sentences=next_sentences,
            previous_sentences=next_sentences,
        )
    else:
        await create_current_text_user(
            telegram_id=user.telegram_id,
            text_id=text_id,
            next_sentences=next_sentences,
            previous_sentences=previous_sentences,
        )

    await message.answer(text_for_user, reply_markup=markup, parse_mode='HTML')


async def get_texts(user: Users):
    main_text, translate_text, text_id = await get_text_for_user(user=user)
    logger.debug(f'Get new text text_id = {text_id}\n{main_text}\n{translate_text}')

    sentences = sent_tokenize(text=main_text.replace('.', '. '), language=languages[user.learn_language])
    translate_sentences = sent_tokenize(text=translate_text.replace('.', '. '), language=languages[user.main_language])
    logger.debug(f'Split sentences\n{sentences}')
    logger.debug(f'\nSplit translate sentences\n{translate_sentences}')
    logger.debug(f'len texts = {len(sentences)}, {len(translate_sentences)}')

    if len(sentences) != len(translate_sentences):
        logger.debug(f'differen len of texts, delete texts')
        delete_text(text_id=text_id)
        await get_texts(user=user)

    return sentences, translate_sentences, text_id
