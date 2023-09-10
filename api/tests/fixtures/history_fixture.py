from datetime import datetime, timedelta
from random import choice, randint

from faker import Faker
from pytest import fixture

from tests.connect_db import db_session
from models import BooksModel, Users, UsersBooksHistory, UsersWordsHistory, Words
from tests.fixtures.test_fixtures_book import book_mock, words_mock
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


@fixture
def history_word_mock(words_mock, telegram_users_mock):
    with db_session() as db:
        word = db.query(Words).first()
        telegram_user = db.query(Users).first()

        history_book = UsersWordsHistory(
            telegram_user_id=telegram_user.telegram_id,
            word_id=word.word_id,
            is_known=False,
            count_view=0,
            correct_answers=0,
            incorrect_answers=0,
            correct_answers_in_row=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.add(history_book)
        db.commit()


@fixture
def history_all_history_words_mock(words_mock, telegram_users_mock):
    with db_session() as db:
        history_word = db.query(UsersWordsHistory).first()
        telegram_user_id = history_word.telegram_user_id
        words = db.query(Words).all()
        for word in words:

            history_word = UsersWordsHistory(
                telegram_user_id=telegram_user_id,
                word_id=word.word_id,
                is_known=choice([True, False]),
                count_view=randint(0, 100),
                correct_answers=randint(0, 100),
                incorrect_answers=randint(0, 100),
                correct_answers_in_row=randint(0, 100),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

            db.add(history_word)
        db.commit()