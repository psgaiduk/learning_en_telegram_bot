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
        cls._url = '/api/v1/history/books'

    def test_add_history_book(self, history_book_not_complete_mock):
        with db_session() as db:
            history_book = db.query(UsersBooksHistory).first()
            assert history_book.end_read is None

        url = f'{self._url}/{history_book.id}/'
        response = self._client.patch(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()

        with db_session() as db:
            db_history_book = db.query(UsersBooksHistory).filter(UsersBooksHistory.id == history_book.id).first()
            assert db_history_book.end_read is not None
            assert db_history_book.end_read == datetime.strptime(response['end_read'], '%Y-%m-%dT%H:%M:%S.%f')
