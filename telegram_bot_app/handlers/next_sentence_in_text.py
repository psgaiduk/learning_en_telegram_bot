from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text as text_filter
from loguru import logger

from db.functions.current_text_user import update_current_text_user
from db.functions.texts_users import create_texts_users
from telegram_bot_app.states import TextStates
from telegram_bot_app.core import dispatcher


@dispatcher.message_handler(text_filter(equals='далее', ignore_case=True), state=TextStates.next_sentence)
async def next_sentence_in_text(message: types.Message, state: FSMContext):

    state_data = await state.get_data()

    user = state_data.get('user')
    logger.debug(f'Get user = {user}')
    next_sentences = state_data.get('next_sentences')

    if next_sentences:
        current_sentence = state_data.get('next_sentences').pop(0)
        previous_sentences = state_data.get('previous_sentences')
        next_sentences = state_data.get('next_sentences')
        logger.debug(f'current sentence\n{current_sentence}')
        await state.update_data({'previous_sentences': previous_sentences, 'next_sentences': next_sentences})

        text_for_user = '\n'.join(
            [
                current_sentence[0],
                '\n<u>Посмотреть перевод:</u>',
                f'<tg-spoiler>{current_sentence[1]}</tg-spoiler>',
                f'\nДо конца осталось: {len(next_sentences)} шт.'
            ])

        await update_current_text_user(
            telegram_id=user.telegram_id,
            next_sentences=next_sentences,
            previous_sentences=next_sentences,
        )

        await message.answer(text_for_user, parse_mode='HTML')
    else:
        text_for_user = 'Поздравляю! Текст закончен.\nЗавтра будет новый!'
        markup = types.ReplyKeyboardRemove()
        text_id = state_data.get('text_id')
        await create_texts_users(user=user, text_id=text_id)

        await state.finish()

        await message.answer(text_for_user, reply_markup=markup, parse_mode='HTML')


@dispatcher.message_handler(state=TextStates.next_sentence)
async def next_sentence_in_text_invalid(message: types.Message):
    """
    If next sentence is invalid
    """
    text_message = 'Нажми кнопку далее или напиши слово далее, чтобы продолжить.'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Далее')

    return await message.reply(text_message, reply_markup=markup)
