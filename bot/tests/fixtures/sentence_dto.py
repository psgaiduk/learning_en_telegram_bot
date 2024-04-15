from pytest import fixture

from dto import NewSentenceDTOModel
from .word_dto import word_new


@fixture
def sentence_with_word(word_new):
    return NewSentenceDTOModel(
        history_sentence_id=1,
        book_id=1,
        order=1,
        sentence_id=1,
        text='test_text',
        text_with_words='test_text_with_word',
        text_with_new_words='test_text_with_new_word',
        translation={'ru': 'test_text'},
        sentence_times='Present Perfect',
        description_time='Description',
        words=[word_new],
    )
