from datetime import datetime

from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import UsersBooksHistory
from settings import settings
from tests.fixtures import (
    create_test_database,
    telegram_users_mock,
    book_mock,
    history_book_not_complete_mock,
    history_book_complete_mock,
    level_en_mock,
    main_language_mock,
    hero_level_mock,
)
from tests.connect_db import db_session


@mark.usefixtures('create_test_database', 'telegram_users_mock', 'book_mock')
class TestGetHistoryBookByIdAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)
        cls._url = '/api/v1/history/books'

    def test_complete_history_book(self, history_book_complete_mock):
        with db_session() as db:
            history_book = db.query(UsersBooksHistory).first()

        url = f'{self._url}/{history_book.id}/'
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()

        assert history_book.end_read == datetime.strptime(response['end_read'], '%Y-%m-%dT%H:%M:%S.%f')
        assert history_book.id == response['id']
        assert history_book.telegram_user_id == response['telegram_user_id']
        assert history_book.book_id == response['book_id']
        assert history_book.start_read == datetime.strptime(response['start_read'], '%Y-%m-%dT%H:%M:%S.%f')

    def test_not_get_history_book_without_api_key(self, history_book_not_complete_mock):
        with db_session() as db:
            history_book = db.query(UsersBooksHistory).first()
            assert history_book.end_read is None

        url = f'{self._url}/{history_book.id}/'
        response = self._client.get(url=url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_get_history_book_with_wrong_api_key(self, history_book_not_complete_mock):
        with db_session() as db:
            history_book = db.query(UsersBooksHistory).first()
            assert history_book.end_read is None

        url = f'{self._url}/{history_book.id}/'
        response = self._client.get(url=url, headers={'X-API-Key': 'wrong_api_key'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_get_history_book_not_found(self, history_book_not_complete_mock):
        with db_session() as db:
            history_book = db.query(UsersBooksHistory).order_by(UsersBooksHistory.id.desc()).first()
            history_book_id = history_book.id + 1

        url = f'{self._url}/{history_book_id}/'
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
