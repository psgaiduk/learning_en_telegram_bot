from pytest import fixture

from tests.connect_db import db_session
from models import BooksModel, LevelsEn
from tests.fixtures.test_fixtures_services import level_en_mock


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
