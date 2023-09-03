from datetime import datetime

from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import BooksModel, Users, UsersBooksHistory
from settings import settings
from tests.fixtures import (
    create_test_database,
    telegram_users_mock,
    book_mock,
    history_book_not_complete_mock,
    level_en_mock,
    main_language_mock,
    hero_level_mock,
)
from tests.connect_db import db_session


@mark.usefixtures('create_test_database', 'telegram_users_mock', 'book_mock')
class TestAddHistoryBookAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)
        cls._url = '/api/v1/history'

    def test_add_history_book(self):
        with db_session() as db:
            telegram_user = db.query(Users).first()
            book = db.query(BooksModel).first()

        url = f'{self._url}/books/{telegram_user.telegram_id}/{book.book_id}/'
        response = self._client.post(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()

        with db_session() as db:
            db_history_book = db.query(UsersBooksHistory).first()
            start_read = datetime.strptime(response['start_read'], '%Y-%m-%dT%H:%M:%S.%f')
            assert db_history_book.telegram_user_id == response['telegram_user_id']
            assert db_history_book.book_id == response['book_id']
            assert db_history_book.end_read == response['end_read'] is None
            assert db_history_book.start_read == start_read is not None

    def test_not_add_history_book_for_telegram_id_not_found(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_user_id = telegram_user.telegram_id + 1
            book = db.query(BooksModel).first()

        url = f'{self._url}/books/{telegram_user_id}/{book.book_id}/'
        response = self._client.post(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_not_add_history_book_for_book_id_not_found(self):
        with db_session() as db:
            telegram_user = db.query(Users).first()
            book = db.query(BooksModel).order_by(BooksModel.book_id.desc()).first()
            book_id = book.book_id + 1

        url = f'{self._url}/books/{telegram_user.telegram_id}/{book_id}/'
        response = self._client.post(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
