from pytest import fixture

from dto import TelegramUserDTOModel
from .sentence_dto import sentence_with_word


@fixture
def telegram_user_with_sentence_and_word(sentence_with_word):
    return TelegramUserDTOModel(
        stage='test_stage',
        user_name='test_name',
        experience=0,
        previous_stage='test_previous_stage',
        telegram_id=1,
        hero_level=None,
        level_en=None,
        main_language=None,
        new_sentence=sentence_with_word,
    )