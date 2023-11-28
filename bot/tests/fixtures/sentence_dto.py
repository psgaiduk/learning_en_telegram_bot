from pytest import fixture

from dto import NewSentenceDTOModel
from .word_dto import word_new


@fixture
def sentence_with_word(word_new):
    return NewSentenceDTOModel(
            history_sentence_id=1,
            book_id=1,
            sentence_id=1,
            text='test_text',
            translation={'ru': 'test_text'},
            words=[word_new],
        )
