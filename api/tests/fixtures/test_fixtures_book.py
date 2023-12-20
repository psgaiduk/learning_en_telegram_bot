from faker import Faker
from pytest import fixture

from tests.connect_db import db_session
from models import BooksModel, LevelsEn, BooksSentences, Words
from tests.fixtures.test_fixtures_services import level_en_mock, type_words_mock


fake = Faker()
fake_ru = Faker('ru_RU')


@fixture
def book_mock(level_en_mock):
    with db_session() as db:
        levels = db.query(LevelsEn).all()

        for level_en in levels:
            book_texts = [
                (
                    'Reading practice to help you understand simple information, words and sentences about ',
                    'known topics. Texts include posters, messages, forms and timetables.'
                ),
            ]

            text_1 = ''.join(book_texts[0])

            books_data = [
                {'title': 'First Book', 'level_en_id': level_en.id, 'author': 'First Author', 'text': text_1},
                {'title': 'Second Book', 'level_en_id': level_en.id, 'author': 'Second Author', 'text': text_1},
                {'title': 'Third Book', 'level_en_id': level_en.id, 'author': 'Third Author', 'text': text_1},
            ]

            for book_data in books_data:
                book = BooksModel(**book_data)
                db.add(book)
            db.commit()


@fixture()
def book_sentences_mock():
    with db_session() as db:

        levels = db.query(LevelsEn).all()

        sentence_id = 0

        for level_en in levels:

            books_in_level = db.query(BooksModel).filter(BooksModel.level_en_id == level_en.id).all()

            for book in books_in_level:

                sentences_data = [
                    {'sentence_id': sentence_id + 1, 'book_id': book.book_id, 'order': 1, 'text': 'First sentence',
                     'translation': {'ru': 'Первое предложение'}, 'sentence_times': 'Present Simple', 'description_time': 'Every day'},
                    {'sentence_id': sentence_id + 2, 'book_id': book.book_id, 'order': 2, 'text': 'Second sentence',
                     'translation': {'ru': 'Второе предложение'}, 'sentence_times': 'Present Simple', 'description_time': 'Every day'},
                    {'sentence_id': sentence_id + 3, 'book_id': book.book_id, 'order': 3, 'text': 'Third sentence',
                     'translation': {'ru': 'Третье предложение'}, 'sentence_times': 'Present Simple', 'description_time': 'Every day'},
                ]

                sentence_id += 3

                for sentence_data in sentences_data:
                    sentence = BooksSentences(**sentence_data)
                    db.add(sentence)

        db.commit()


@fixture
def words_mock(level_en_mock, type_words_mock, book_mock, book_sentences_mock):
    with db_session() as db:

        levels = db.query(LevelsEn).all()

        for level_en in levels:

            books_in_level = db.query(BooksModel).filter(BooksModel.level_en_id == level_en.id).all()

            for book in books_in_level:

                for sentence in book.books_sentences:

                    words_data = [
                        {'type_word_id': 1, 'word': fake.word(), 'translation': {'ru': fake_ru.word()}},
                        {'type_word_id': 2, 'word': fake.word(), 'translation': {'ru': fake_ru.word()}},
                        {'type_word_id': 3, 'word': fake.word(), 'translation': {'ru': fake_ru.word()}},
                    ]

                    for word_data in words_data:
                        word = Words(**word_data)
                        db.add(word)
                        sentence.words.append(word)

        db.commit()
