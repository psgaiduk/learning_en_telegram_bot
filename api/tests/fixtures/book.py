from pytest import fixture

from database import get_db
from models import BooksModel, LevelsEn
from .services import level_en_mock


@fixture
def book_mock(level_en_mock):
    with get_db() as db:
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
