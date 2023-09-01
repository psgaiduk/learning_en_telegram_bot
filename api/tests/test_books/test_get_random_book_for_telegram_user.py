from datetime import datetime

from fastapi.testclient import TestClient
from main import app
from fastapi import status
from pytest import mark, fail

from tests.connect_db import db_session
from tests.fixtures import (
    create_test_database,
    book_mock,
    book_sentences_mock,
    words_mock,
    telegram_users_mock, 
    level_en_mock,
    hero_level_mock,
    main_language_mock,
    type_words_mock,
)
from models import BooksModel, Users, UsersBooksHistory
from settings import settings


@mark.usefixtures('create_test_database', 'book_mock', 'telegram_users_mock')
class TestGetRandomBookAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)

    def test_good_get_random_book_for_user(self):
        with db_session() as db:
            user = db.query(Users).first()

            if not user:
                fail('Test data is not initialized properly.')

            response = self._client.get(f'/api/v1/books/get-random-book/{user.telegram_id}/', headers=self._headers)
            assert response.status_code == status.HTTP_200_OK

            response = response.json()
            assert response['level_en_id'] == user.level_en_id

    def test_not_found_get_random_book_for_user(self):
        with db_session() as db:
            user = db.query(Users).first()
            all_books_in_this_levels = db.query(BooksModel).filter(BooksModel.level_en_id == user.level_en_id).all()

            for book in all_books_in_this_levels:
                user_history = UsersBooksHistory(
                    telegram_user_id=user.telegram_id,
                    book_id=book.book_id,
                    start_read=datetime.utcnow(),
                    end_read=datetime.utcnow(),
                )

                db.add(user_history)

            db.commit()

            response = self._client.get(f'/api/v1/books/get-random-book/{user.telegram_id}/', headers=self._headers)
            assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_not_get_random_book_without_api_key(self):
        with db_session() as db:
            user = db.query(Users).first()

            if not user:
                fail('Test data is not initialized properly.')

            response = self._client.get(f'/api/v1/books/get-random-book/{user.telegram_id}/')
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

