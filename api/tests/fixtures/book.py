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

            books_data = [
                {'title': 'First Book', 'level_en_id': level_en.id, 'author': 'First Author', 'text': book_texts[0]},
                {'title': 'Second Book', 'level_en_id': level_en.id, 'author': 'Second Author', 'text': book_texts[0]},
                {'title': 'Third Book', 'level_en_id': level_en.id, 'author': 'Third Author', 'text': book_texts[0]},
            ]

            for book_data in books_data:
                book = BooksModel(**book_data)
                db.add(book)
            db.commit()
