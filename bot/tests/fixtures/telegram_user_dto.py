from pytest import fixture

from dto import TelegramUserDTOModel
from .sentence_dto import sentence_with_word
from .level_en_dto import level_en


@fixture
def telegram_user_with_sentence_and_word(sentence_with_word, level_en):
    return TelegramUserDTOModel(
        stage='test_stage',
        user_name='test_name',
        experience=0,
        previous_stage='test_previous_stage',
        telegram_id=1,
        hero_level=None,
        level_en=level_en,
        main_language=None,
        new_sentence=sentence_with_word,
    )