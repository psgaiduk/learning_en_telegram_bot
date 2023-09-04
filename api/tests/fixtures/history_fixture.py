from datetime import datetime, timedelta

from faker import Faker
from pytest import fixture

from tests.connect_db import db_session
from models import BooksModel, Users, UsersBooksHistory
from tests.fixtures.test_fixtures_book import book_mock
from tests.fixtures.telegram_users_fixture import telegram_users_mock


fake = Faker()
fake_ru = Faker('ru_RU')


@fixture
def history_book_not_complete_mock(book_mock, telegram_users_mock):
    with db_session() as db:
        book = db.query(BooksModel).first()
        telegram_user = db.query(Users).first()

        history_book = UsersBooksHistory(
            telegram_user_id=telegram_user.telegram_id,
            book_id=book.book_id,
        )

        db.add(history_book)
        db.commit()


@fixture
def history_book_complete_mock(book_mock, telegram_users_mock):
    with db_session() as db:
        book = db.query(BooksModel).first()
        telegram_user = db.query(Users).first()

        history_book = UsersBooksHistory(
            telegram_user_id=telegram_user.telegram_id,
            book_id=book.book_id,
            start_read=datetime.utcnow() - timedelta(days=3),
            end_read=datetime.utcnow(),
        )

        db.add(history_book)
        db.commit()
