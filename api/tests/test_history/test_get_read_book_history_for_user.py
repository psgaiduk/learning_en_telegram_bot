from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import Users, UsersBooksHistory
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


@mark.usefixtures("create_test_database", "telegram_users_mock", "book_mock")
class TestAddHistoryBookAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {"X-API-Key": settings.api_key}
        cls._client = TestClient(app)
        cls._url = "/api/v1/history/books/telegram_user"

    def test_get_history_user(self, history_book_complete_mock):
        with db_session() as db:
            book_history = db.query(UsersBooksHistory).first()
            telegram_user_id = book_history.telegram_user_id

            history_books_user = (
                db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_user_id).all()
            )
        url = f"{self._url}/{telegram_user_id}/"
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()

        assert len(history_books_user) == len(response)

        with db_session() as db:
            new_history = UsersBooksHistory(
                telegram_user_id=telegram_user_id,
                book_id=book_history.book_id,
            )

            db.add(new_history)
            db.commit()
            db.refresh(new_history)

            history_books_user = (
                db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_user_id).all()
            )

        url = f"{self._url}/{telegram_user_id}/"
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()

        assert len(history_books_user) == len(response)

    def test_not_get_history_book_without_api_key(self, history_book_not_complete_mock):
        with db_session() as db:
            book_history = db.query(UsersBooksHistory).first()
            telegram_user_id = book_history.telegram_user_id

        url = f"{self._url}/{telegram_user_id}/"
        response = self._client.get(url=url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_get_history_book_with_wrong_api_key(self, history_book_not_complete_mock):
        with db_session() as db:
            book_history = db.query(UsersBooksHistory).first()
            telegram_user_id = book_history.telegram_user_id

        url = f"{self._url}/{telegram_user_id}/"

        response = self._client.get(url=url, headers={"X-API-Key": "wrong_api_key"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_get_history_book_not_found(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id).first()

        url = f"{self._url}/{telegram_user.telegram_id}/"
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
