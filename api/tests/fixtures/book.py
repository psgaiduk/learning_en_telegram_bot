from pytest import fixture


@fixture
def mock_book():
    word = {
        'word_id': 1,
        'type_word_id': 1,
        'word': "Hello",
        'translation': {"ru": "Привет"}
    }

    sentence = {
        'sentence_id': 1,
        'book_id': 1,
        'order': 1,
        'text': "Hello world",
        'translation': {"ru": "Привет, мир"},
        'words': [word]
    }

    book = {
        'book_id': 1,
        'title': "Test Book",
        'level_en_id': 1,
        'author': "Author",
        'books_sentences': [sentence]
    }

    class MockModel:
        def __init__(self, **kwargs):
            self.__dict__ = kwargs

    return MockModel(**book)
