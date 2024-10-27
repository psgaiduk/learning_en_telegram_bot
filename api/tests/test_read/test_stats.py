from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import (
    Words,
    Users,
    UsersWordsHistory,
)
from settings import settings
from tests.fixtures import *
from tests.connect_db import db_session


@mark.usefixtures(
    "create_test_database",
    "telegram_users_mock",
    "book_mock",
    "book_sentences_mock",
    "words_mock",
)
class TestReadApi:

    def setup_method(self):
        self._headers = {"X-API-Key": settings.api_key}
        self._client = TestClient(app)
        self._url = "/api/v1/read/stats"

    def test_get_stats_for_user_without_data(self):

        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id

        url = f"{self._url}/{telegram_id}/"
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        assert "detail" in response.json()
        response = response.json()["detail"]
        assert response["count_of_words"] == 0
        assert response["count_of_new_words"] == 0
        assert response["time_to_next_word"] == 0

    # def test_get_stats_for_user_with_read_sentences(self):

    #     with db_session() as db:
    #         telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
    #         telegram_id = telegram_user.telegram_id
    #         users_history_book = (
    #             db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
    #         )
    #         assert users_history_book is None
    #         users_history_book_sentence = (
    #             db.query(UsersBooksSentencesHistory)
    #             .filter(UsersBooksSentencesHistory.telegram_user_id == telegram_id)
    #             .first()
    #         )
    #         assert users_history_book_sentence is None
    #         first_book = db.query(BooksModel).first()
    #         new_history_book = UsersBooksHistory(
    #             telegram_user_id=telegram_id,
    #             book_id=first_book.book_id,
    #             start_read=datetime.now(),
    #             end_read=datetime.now(),
    #         )
    #         db.add(new_history_book)
    #         sentence = (
    #             db.query(BooksSentences)
    #             .filter(BooksSentences.book_id == first_book.book_id, BooksSentences.order == 1)
    #             .first()
    #         )
    #         new_history_sentence = UsersBooksSentencesHistory(
    #             telegram_user_id=telegram_id,
    #             sentence_id=sentence.sentence_id,
    #             check_words=[],
    #             is_read=True,
    #         )
    #         db.add(new_history_sentence)
    #         db.commit()

    #     url = f"{self._url}/{telegram_id}/"
    #     response = self._client.get(url=url, headers=self._headers)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert "detail" in response.json()
    #     response = response.json()["detail"]
    #     assert response["count_of_sentences"] == 1
    #     assert response["count_of_words"] == 0
    #     assert response["count_of_new_words"] == 0
    #     assert response["time_to_next_word"] == 0

    #     with db_session() as db:
    #         first_book = db.query(BooksModel).first()
    #         sentence = (
    #             db.query(BooksSentences)
    #             .filter(BooksSentences.book_id == first_book.book_id, BooksSentences.order == 2)
    #             .first()
    #         )
    #         new_history_sentence = UsersBooksSentencesHistory(
    #             telegram_user_id=telegram_id,
    #             sentence_id=sentence.sentence_id,
    #             check_words=[],
    #             is_read=True,
    #         )
    #         db.add(new_history_sentence)
    #         db.commit()

    #     url = f"{self._url}/{telegram_id}/"
    #     response = self._client.get(url=url, headers=self._headers)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert "detail" in response.json()
    #     response = response.json()["detail"]
    #     assert response["count_of_sentences"] == 2
    #     assert response["count_of_words"] == 0
    #     assert response["count_of_new_words"] == 0
    #     assert response["time_to_next_word"] == 0

    def test_get_stats_for_user_with_new_words(self):

        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id
            word = db.query(Words).first()
            new_history_word = UsersWordsHistory(
                telegram_user_id=telegram_id,
                word_id=word.word_id,
                is_known=True,
                correct_answers_in_row=0,
                repeat_datetime=datetime.now(timezone.utc) - timedelta(hours=5),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            db.add(new_history_word)
            db.commit()

        url = f"{self._url}/{telegram_id}/"
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        assert "detail" in response.json()
        response = response.json()["detail"]
        assert response["count_of_words"] == 1
        assert response["count_of_new_words"] == 1
        assert response["time_to_next_word"] == 0

    def test_get_stats_for_user_with_new_words_without_repeat_words(self):

        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id
            words = db.query(Words).all()
            word_first = words[0]
            word_second = words[1]
            new_history_word = UsersWordsHistory(
                telegram_user_id=telegram_id,
                word_id=word_first.word_id,
                is_known=True,
                correct_answers_in_row=0,
                repeat_datetime=datetime.now(timezone.utc) + timedelta(hours=5),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            db.add(new_history_word)
            new_history_word_second = UsersWordsHistory(
                telegram_user_id=telegram_id,
                word_id=word_second.word_id,
                is_known=True,
                correct_answers_in_row=0,
                repeat_datetime=datetime.now(timezone.utc) + timedelta(hours=1),
                created_at=datetime.now(timezone.utc) - timedelta(hours=90),
                updated_at=datetime.now(timezone.utc),
            )
            db.add(new_history_word_second)
            db.commit()

        url = f"{self._url}/{telegram_id}/"
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        assert "detail" in response.json()
        response = response.json()["detail"]
        assert response["count_of_words"] == 2
        assert response["count_of_new_words"] == 1
        assert response["time_to_next_word"] == 59

    def test_not_get_stats_for_user_without_key(self):
        headers = {}
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id

        url = f"{self._url}/{telegram_id}/"
        response = self._client.get(url=url, headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_get_stats_for_user_with_wrong_key(self):
        headers = {"X-API-Key": "wrong"}
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id

        url = f"{self._url}/{telegram_id}/"
        response = self._client.get(url=url, headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_get_stats_for_not_user(self):

        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id + 1

        url = f"{self._url}/{telegram_id}/"
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
