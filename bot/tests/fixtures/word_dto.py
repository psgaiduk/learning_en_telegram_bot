from datetime import datetime

from pytest import fixture

from dto import WordDTOModel


@fixture
def word_new():
    return WordDTOModel(
        word_id=1,
        word='test',
        type_word_id=1,
        translation={'ru': 'тест'},
        is_known=False,
        count_view=0,
        correct_answers=0,
        incorrect_answers=0,
        correct_answers_in_row=0,
        increase_factor=2.0,
        interval_repeat=600,
        repeat_datetime=datetime.utcnow(),
    )


@fixture
def word_second():
    return WordDTOModel(
        word_id=2,
        word='second',
        type_word_id=1,
        translation={'ru': 'второй'},
        is_known=False,
        count_view=0,
        correct_answers=0,
        incorrect_answers=0,
        correct_answers_in_row=0,
        increase_factor=2.0,
        interval_repeat=600,
        repeat_datetime=datetime.utcnow(),
    )
