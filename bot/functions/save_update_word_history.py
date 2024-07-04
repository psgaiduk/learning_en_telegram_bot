from loguru import logger

from functions.update_data_by_api import update_data_by_api


async def save_word_history(callback_query):
    is_known = False
    start_text_message = 'Хорошо. Повторим потом ещё раз.\n\n'
    word_id = int(callback_query.data.split('_')[-1])
    if 'know_word_true' in callback_query.data:
        is_known = True
        start_text_message = 'Отлично! Давай продолжим.\n\n'

    data_for_update_word = {
        'telegram_user_id': callback_query.from_user.id,
        'word_id': word_id,
        'is_known': is_known,
    }

    logger.debug(f'data_for_update_word: {data_for_update_word}')

    is_update_history = await update_data_by_api(
        telegram_id=callback_query.from_user.id,
        params_for_update=data_for_update_word,
        url_for_update=f'history/words',
    )

    logger.debug(f'is_update_history: {is_update_history}')

    return is_update_history, start_text_message
