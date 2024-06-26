from datetime import datetime, timedelta

from aiogram.types import CallbackQuery
from loguru import logger

from dto import WordDTOModel
from functions.update_data_by_api import update_data_by_api


async def update_learn_word(message: CallbackQuery, word: WordDTOModel):
    if 'yes' in message.data:
        word.increase_factor += 0.05
        word.interval_repeat *= 0.05
        if word.increase_factor > 2:
            word.increase_factor = 2
    else:
        word.increase_factor -= 0.1
        word.interval_repeat = 60
        if word.increase_factor < 1.1:
            word.increase_factor = 1.1

    word.repeat_datetime = datetime.now() + timedelta(seconds=word.interval_repeat)

    data_for_update_word = {
        'telegram_user_id': message.from_user.id,
        'word_id': word.word_id,
        'increase_factor': word.increase_factor,
        'interval_repeat': word.interval_repeat,
        'repeat_datetime': word.repeat_datetime,
    }

    logger.debug(f'data_for_update_word: {data_for_update_word}')

    is_update_history = await update_data_by_api(
        telegram_id=message.from_user.id,
        params_for_update=data_for_update_word,
        url_for_update='history/words',
    )

    logger.debug(f'is_update_history: {is_update_history}')
    return is_update_history
