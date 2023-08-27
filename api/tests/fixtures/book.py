from pytest import fixture

from database import get_db
from models import BooksModel


@fixture
def book_mock():
    with get_db() as db:
        book_first = BooksModel(
            title='First Book',
            level_en_id=1,
            author='First Author',
            text='Reading practice to help you understand simple information, words and sentences about known topics.'
                 ' Texts include posters, messages, forms and timetables.',
        )
        book_second = BooksModel(
            title='First Book',
            level_en_id=1,
            author='First Author',
            text='Reading practice to help you understand simple information, words and sentences about known topics.'
                 ' Texts include posters, messages, forms and timetables.',
        )
        book_third = BooksModel(
            title='First Book',
            level_en_id=1,
            author='First Author',
            text='Reading practice to help you understand simple information, words and sentences about known topics.'
                 ' Texts include posters, messages, forms and timetables.',
        )

        db.add(book_first)
        db.add(book_second)
        db.add(book_third)
        db.commit()
