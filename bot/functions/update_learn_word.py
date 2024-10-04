from datetime import datetime, timedelta

from aiogram.types import CallbackQuery
from loguru import logger

from dto import WordDTOModel
from functions.update_data_by_api import update_data_by_api


async def update_learn_word(message: CallbackQuery, word: WordDTOModel) -> bool:
    """
    Function for update learn word.

    :params message: callback from telegram.
    :params word: learn word.
    :return: status update learn word.
    """
    logger.debug(f"word = {word}")
    word.count_view += 1
    if "yes" in message.data:
        word.correct_answers += 1
        word.correct_answers_in_row += 1
        word.increase_factor += 0.1
        if word.increase_factor > 2.5:
            word.increase_factor = 2.5

        if word.interval_repeat == 1:
            word.interval_repeat = 86400
        else:
            word.interval_repeat *= word.increase_factor
    else:
        word.increase_factor -= 0.2
        word.interval_repeat = 1
        word.correct_answers_in_row = 0
        word.incorrect_answers += 1
        if word.increase_factor < 1.1:
            word.increase_factor = 1.1

    word.repeat_datetime = datetime.now() + timedelta(seconds=word.interval_repeat)

    data_for_update_word = {
        "telegram_user_id": message.from_user.id,
        "word_id": word.word_id,
        "increase_factor": word.increase_factor,
        "interval_repeat": word.interval_repeat,
        "repeat_datetime": f"{word.repeat_datetime}",
        "count_view": word.count_view,
        "correct_answers_in_row": word.correct_answers_in_row,
        "incorrect_answers": word.incorrect_answers,
    }

    logger.debug(f"data_for_update_word: {data_for_update_word}")

    is_update_history = await update_data_by_api(
        telegram_id=message.from_user.id,
        params_for_update=data_for_update_word,
        url_for_update="history/words",
    )

    logger.debug(f"is_update_history: {is_update_history}")
    return is_update_history
