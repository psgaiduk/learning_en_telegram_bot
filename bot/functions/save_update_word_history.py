from datetime import datetime, timedelta

from loguru import logger

from functions.update_data_by_api import update_data_by_api


async def save_word_history(callback_query):
    start_text_message = 'Хорошо. Повторим потом ещё раз.\n\n'
    word_id = int(callback_query.data.split('_')[-1])
    increase_factor = 2
    interval_repeat = 60
    if 'know_word_true' in callback_query.data:
        interval_repeat = 3600
        start_text_message = 'Отлично! Давай продолжим.\n\n'

    repeat_datetime = datetime.now() + timedelta(seconds=interval_repeat)

    data_for_update_word = {
        'telegram_user_id': callback_query.from_user.id,
        'word_id': word_id,
        'is_known': True,
        'increase_factor': increase_factor,
        'interval_repeat': interval_repeat,
        'repeat_datetime': f'{repeat_datetime}',
    }

    logger.debug(f'data_for_update_word: {data_for_update_word}')

    is_update_history = await update_data_by_api(
        telegram_id=callback_query.from_user.id,
        params_for_update=data_for_update_word,
        url_for_update=f'history/words',
    )

    logger.debug(f'is_update_history: {is_update_history}')

    return is_update_history, start_text_message
