from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger
from nltk.tokenize import sent_tokenize

from db.models import Users
from db.functions.users import get_user_by_telegram_id, create_user
from db.functions.texts import get_text_for_user, delete_text
from db.functions.texts_users import get_today_text_by_telegram_id
from telegram_bot_app.core import dispatcher
from telegram_bot_app.states import TextStates

languages = {'ru': 'russian', 'en': 'english', 'fr': 'french', 'es': 'spanish', 'ge': 'german'}


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

    is_complete_text_today = await get_today_text_by_telegram_id(telegram_id=user.telegram_id)
    logger.debug(f'check have user text today = {is_complete_text_today}')
    if is_complete_text_today:
        logger.debug(f'user today have text, send about this')
        await message.answer('Вы сегодня уже прочитали текст, завтра будет новый.', parse_mode='HTML')
        return

    sentences, translate_sentences, text_id = await get_texts(user=user)

    sentences_for_user = []
    for index, sentence in enumerate(sentences):
        if not sentence:
            continue
        sentence_on_main_language = sentence
        sentence_translate = translate_sentences[index]
        sentences_for_user.append((sentence_on_main_language.strip(), sentence_translate.strip()))

    logger.debug(f'List sentences and translate:\n{sentences_for_user}')

    current_sentence = sentences_for_user.pop(0)
    previous_sentences = [current_sentence]
    next_sentences = sentences_for_user

    logger.debug(f'current sentence\n{current_sentence}')

    await state.set_data(
        {
            'previous_sentences': previous_sentences,
            'next_sentences': next_sentences,
            'user': user,
            'text_id': text_id,
        }
    )

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Далее')

    text_for_user = '\n'.join(
        [
            current_sentence[0],
            '\n<u>Посмотреть перевод:</u>',
            f'<tg-spoiler>{current_sentence[1]}</tg-spoiler>',
            f'\nДо конца осталось: {len(next_sentences)} шт.'
        ])

    await TextStates.next_sentence.set()

    await message.answer(text_for_user, reply_markup=markup, parse_mode='HTML')


async def get_texts(user: Users):
    main_text, translate_text, text_id = await get_text_for_user(user=user)
    logger.debug(f'Get new text text_id = {text_id}\n{main_text}\n{translate_text}')

    sentences = sent_tokenize(text=main_text.replace('.', '. '), language=languages[user.learn_language])
    translate_sentences = sent_tokenize(text=translate_text.replace('.', '. '), language=languages[user.main_language])
    logger.debug(f'Split sentences\n{sentences}')
    logger.debug(f'\nSplit translate sentences\n{translate_sentences}')

    if len(sentences) != len(translate_sentences):
        delete_text(text_id=text_id)
        await get_texts(user=user)

    return sentences, translate_sentences, text_id
