from datetime import datetime

from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import (
    BooksModel,
    Users,
    UsersBooksHistory,
    UsersBooksSentencesHistory,
    BooksSentences,
    UsersWordsHistory,
)
from settings import settings
from tests.fixtures import *
from tests.connect_db import db_session


@mark.usefixtures(
    "create_test_database",
    "telegram_users_mock",
    "book_mock",
    "words_mock",
)
class TestReadApi:

    def setup_method(self):
        self._headers = {"X-API-Key": settings.api_key}
        self._client = TestClient(app)
        self._url = "/api/v1/read"

    def test_get_first_sentence_for_not_read_early(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id
            users_history_book = (
                db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
            )
            assert users_history_book is None
            users_history_book_sentence = (
                db.query(UsersBooksSentencesHistory)
                .filter(UsersBooksSentencesHistory.telegram_user_id == telegram_id)
                .first()
            )
            assert users_history_book_sentence is None

        url = f"{self._url}/{telegram_id}/"
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()["detail"]

        with db_session() as db:
            users_history_book = (
                db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
            )
            assert users_history_book is not None
            book_id = users_history_book.book_id
            assert users_history_book.start_read is not None
            assert users_history_book.end_read is None
            users_history_book_sentence = (
                db.query(UsersBooksSentencesHistory)
                .filter(UsersBooksSentencesHistory.telegram_user_id == telegram_id)
                .first()
            )
            assert users_history_book_sentence is not None
            assert users_history_book_sentence.id == response["history_sentence_id"]
            assert users_history_book_sentence.is_read is False
            assert users_history_book_sentence.sentence_id == response["sentence_id"]
            assert users_history_book_sentence.telegram_user_id == telegram_id
            book = db.query(BooksModel).filter(BooksModel.book_id == book_id).first()
            assert f"{book.author} - {book.title}" in response["text"]
            assert len(response["words"]) <= 5
            sentence = db.query(BooksSentences).filter(BooksSentences.sentence_id == response["sentence_id"]).first()
            assert sentence.order == 1
            assert book.title == response["book_title"]
            assert sentence.tg_audio_sentence.audio_id == response["tg_audio_id"]

            """
            { 'translation': {'ru': 'некоторый'}, 'is_known': False, 'count_view': 0, 'correct_answers': 0, 'incorrect_answers': 0, 'correct_answers_in_row': 0, 'increase_factor': 0.0, 'interval_repeat': 0, 'repeat_datetime': '2024-09-22T06:04:50.390282'}
            """

            for word in response["words"]:
                assert "type_word_id" in word
                assert isinstance(word["type_word_id"], int)
                assert 0 < word["type_word_id"] < 4
                assert "word_id" in word
                assert isinstance(word["word_id"], int)
                assert "word" in word
                assert isinstance(word["word"], str)
                assert "transcription" in word
                assert isinstance(word["transcription"], str)
                assert "part_of_speech" in word
                assert isinstance(word["part_of_speech"], str)
                assert "translation" in word
                assert isinstance(word["translation"], dict)
                assert "ru" in word["translation"]
                assert "is_known" in word
                assert isinstance(word["is_known"], bool)
                assert "count_view" in word
                assert isinstance(word["count_view"], int)
                assert "correct_answers" in word
                assert isinstance(word["correct_answers"], int)
                assert "incorrect_answers" in word
                assert isinstance(word["incorrect_answers"], int)
                assert "correct_answers_in_row" in word
                assert isinstance(word["correct_answers_in_row"], int)
                assert "increase_factor" in word
                assert isinstance(word["increase_factor"], float)
                assert "interval_repeat" in word
                assert isinstance(word["interval_repeat"], int)
                assert "repeat_datetime" in word
                assert isinstance(word["repeat_datetime"], str)

    def test_get_first_sentence_for_not_read_earl_with_read_words(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id
            users_history_book = (
                db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
            )
            assert users_history_book is None
            users_history_book_sentence = (
                db.query(UsersBooksSentencesHistory)
                .filter(UsersBooksSentencesHistory.telegram_user_id == telegram_id)
                .first()
            )
            assert users_history_book_sentence is None
            first_book = db.query(BooksModel).first()
            books_to_add_history = db.query(BooksModel).filter(BooksModel.book_id != first_book.book_id).all()
            for book in books_to_add_history:
                new_history_entry = UsersBooksHistory(
                    telegram_user_id=telegram_id,
                    book_id=book.book_id,
                    start_read=datetime.now(),
                    end_read=datetime.now(),
                )
                db.add(new_history_entry)

            first_sentence = db.query(BooksSentences).filter(BooksSentences.book_id == first_book.book_id).first()
            assert first_sentence.order == 1
            words_from_first_sentence = first_sentence.words
            first_word = words_from_first_sentence[0]

            new_history_learn_word = UsersWordsHistory(
                telegram_user_id=telegram_id,
                word_id=first_word.word_id,
                is_known=True,
                repeat_datetime=datetime.now(),
            )
            db.add(new_history_learn_word)
            db.commit()

        url = f"{self._url}/{telegram_id}/"
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()["detail"]

        with db_session() as db:
            assert len(response["words"]) == len(words_from_first_sentence) - 1

    def test_get_first_sentence_for_next_read_book(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id
            users_history_book = (
                db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
            )
            assert users_history_book is None
            old_book = (
                db.query(BooksModel)
                .filter(
                    BooksModel.level_en_id == telegram_user.level_en_id,
                    BooksModel.title == "First Book - Part 1",
                )
                .first()
            )
            old_book_id = old_book.book_id
            history_book = UsersBooksHistory(
                telegram_user_id=telegram_id,
                book_id=old_book.book_id,
                start_read=datetime.utcnow(),
                end_read=datetime.utcnow(),
            )
            db.add(history_book)
            db.commit()

        url = f"{self._url}/{telegram_id}/"
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()["detail"]

        with db_session() as db:
            assert old_book_id != response["book_id"]
            users_history_book = (
                db.query(UsersBooksHistory)
                .filter(
                    UsersBooksHistory.telegram_user_id == telegram_id,
                    UsersBooksHistory.book_id == response["book_id"],
                )
                .first()
            )
            assert users_history_book is not None
            book_id = users_history_book.book_id
            assert users_history_book.start_read is not None
            assert users_history_book.end_read is None
            users_history_book_sentence = (
                db.query(UsersBooksSentencesHistory)
                .filter(
                    UsersBooksSentencesHistory.telegram_user_id == telegram_id,
                    UsersBooksSentencesHistory.sentence_id == response["sentence_id"],
                )
                .first()
            )
            assert users_history_book_sentence is not None
            assert users_history_book_sentence.is_read is False
            assert users_history_book_sentence.sentence_id == response["sentence_id"]
            assert users_history_book_sentence.telegram_user_id == telegram_id
            book = db.query(BooksModel).filter(BooksModel.book_id == book_id).first()
            assert f"{book.author} - {book.title}" in response["text"]
            assert len(response["words"]) <= 5
            sentence = db.query(BooksSentences).filter(BooksSentences.sentence_id == response["sentence_id"]).first()
            assert sentence.order == 1
            assert sentence.tg_audio_sentence.audio_id == response["tg_audio_id"]
            assert users_history_book_sentence.id == response["history_sentence_id"]
            assert "- part 2" in response["text"].lower()

    def test_get_first_sentence_for_random_read_book(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id
            users_history_book = (
                db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
            )
            assert users_history_book is None
            old_book = (
                db.query(BooksModel)
                .filter(
                    BooksModel.level_en_id == telegram_user.level_en_id,
                    BooksModel.title == "Second Book",
                )
                .first()
            )
            old_book_id = old_book.book_id
            history_book = UsersBooksHistory(
                telegram_user_id=telegram_id,
                book_id=old_book.book_id,
                start_read=datetime.utcnow(),
                end_read=datetime.utcnow(),
            )
            db.add(history_book)
            db.commit()

        url = f"{self._url}/{telegram_id}/"
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()["detail"]

        with db_session() as db:
            assert old_book_id != response["book_id"]
            users_history_book = (
                db.query(UsersBooksHistory)
                .filter(
                    UsersBooksHistory.telegram_user_id == telegram_id,
                    UsersBooksHistory.book_id == response["book_id"],
                )
                .first()
            )
            assert users_history_book is not None
            book_id = users_history_book.book_id
            assert users_history_book.start_read is not None
            assert users_history_book.end_read is None
            users_history_book_sentence = (
                db.query(UsersBooksSentencesHistory)
                .filter(
                    UsersBooksSentencesHistory.telegram_user_id == telegram_id,
                    UsersBooksSentencesHistory.sentence_id == response["sentence_id"],
                )
                .first()
            )
            assert users_history_book_sentence is not None
            assert users_history_book_sentence.is_read is False
            assert users_history_book_sentence.sentence_id == response["sentence_id"]
            assert users_history_book_sentence.telegram_user_id == telegram_id
            book = db.query(BooksModel).filter(BooksModel.book_id == book_id).first()
            assert f"{book.author} - {book.title}" in response["text"]
            assert len(response["words"]) <= 5
            sentence = db.query(BooksSentences).filter(BooksSentences.sentence_id == response["sentence_id"]).first()
            assert sentence.order == 1
            assert users_history_book_sentence.id == response["history_sentence_id"]
            assert sentence.tg_audio_sentence.audio_id == response["tg_audio_id"]
            assert "- part 2" not in response["text"].lower()

    def test_get_first_sentence_after_last_sentence(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id
            users_history_book = (
                db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
            )
            assert users_history_book is None
            old_book = db.query(BooksModel).filter(BooksModel.level_en_id == telegram_user.level_en_id).first()
            old_book_id = old_book.book_id
            history_book = UsersBooksHistory(
                telegram_user_id=telegram_id,
                book_id=old_book.book_id,
                start_read=datetime.utcnow(),
            )
            db.add(history_book)
            sentences = db.query(BooksSentences).filter(BooksSentences.book_id == old_book_id).all()
            for sentence in sentences:
                history_book_sentence = UsersBooksSentencesHistory(
                    telegram_user_id=telegram_id,
                    sentence_id=sentence.sentence_id,
                    is_read=True,
                    created_at=datetime.utcnow(),
                )
                db.add(history_book_sentence)
            db.commit()

        url = f"{self._url}/{telegram_id}/"
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()["detail"]

        with db_session() as db:
            assert old_book_id != response["book_id"]
            users_history_book = (
                db.query(UsersBooksHistory)
                .filter(
                    UsersBooksHistory.telegram_user_id == telegram_id,
                    UsersBooksHistory.book_id == response["book_id"],
                )
                .first()
            )
            assert users_history_book is not None
            book_id = users_history_book.book_id
            assert users_history_book.start_read is not None
            assert users_history_book.end_read is None
            users_history_book_sentence = (
                db.query(UsersBooksSentencesHistory)
                .filter(
                    UsersBooksSentencesHistory.telegram_user_id == telegram_id,
                    UsersBooksSentencesHistory.sentence_id == response["sentence_id"],
                )
                .first()
            )
            assert users_history_book_sentence is not None
            assert users_history_book_sentence.is_read is False
            assert users_history_book_sentence.sentence_id == response["sentence_id"]
            assert users_history_book_sentence.telegram_user_id == telegram_id
            assert users_history_book_sentence.id == response["history_sentence_id"]
            book = db.query(BooksModel).filter(BooksModel.book_id == book_id).first()
            assert f"{book.author} - {book.title}" in response["text"]
            assert len(response["words"]) <= 5
            sentence = db.query(BooksSentences).filter(BooksSentences.sentence_id == response["sentence_id"]).first()
            assert sentence.order == 1
            assert sentence.tg_audio_sentence.audio_id == response["tg_audio_id"]

            old_book_history = (
                db.query(UsersBooksHistory)
                .filter(
                    UsersBooksHistory.telegram_user_id == telegram_id,
                    UsersBooksHistory.book_id == old_book_id,
                )
                .first()
            )
            assert old_book_history is not None
            assert old_book_history.end_read is not None

    def test_get_next_sentence_from_book(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id
            users_history_book = (
                db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
            )
            assert users_history_book is None
            old_book = db.query(BooksModel).filter(BooksModel.level_en_id == telegram_user.level_en_id).first()
            old_book_id = old_book.book_id
            history_book = UsersBooksHistory(
                telegram_user_id=telegram_id,
                book_id=old_book.book_id,
                start_read=datetime.utcnow(),
            )
            db.add(history_book)
            first_sentence = (
                db.query(BooksSentences)
                .filter(BooksSentences.book_id == old_book_id)
                .order_by(BooksSentences.order.asc())
                .first()
            )
            history_book_sentence = UsersBooksSentencesHistory(
                telegram_user_id=telegram_id,
                sentence_id=first_sentence.sentence_id,
                is_read=True,
            )
            db.add(history_book_sentence)
            db.commit()

        url = f"{self._url}/{telegram_id}/"
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()["detail"]

        with db_session() as db:
            assert old_book_id == response["book_id"]
            users_history_book = (
                db.query(UsersBooksHistory)
                .filter(
                    UsersBooksHistory.telegram_user_id == telegram_id,
                    UsersBooksHistory.book_id == response["book_id"],
                )
                .first()
            )
            assert users_history_book is not None
            assert users_history_book.start_read is not None
            assert users_history_book.end_read is None
            users_history_book_sentence = (
                db.query(UsersBooksSentencesHistory)
                .filter(
                    UsersBooksSentencesHistory.telegram_user_id == telegram_id,
                    UsersBooksSentencesHistory.sentence_id == response["sentence_id"],
                )
                .first()
            )
            assert users_history_book_sentence is not None
            assert users_history_book_sentence.is_read is False
            assert users_history_book_sentence.sentence_id == response["sentence_id"]
            assert users_history_book_sentence.telegram_user_id == telegram_id
            assert users_history_book_sentence.id == response["history_sentence_id"]
            assert len(response["words"]) <= 5
            sentence = db.query(BooksSentences).filter(BooksSentences.sentence_id == response["sentence_id"]).first()
            assert sentence.order == 2

            old_book_history = (
                db.query(UsersBooksHistory)
                .filter(
                    UsersBooksHistory.telegram_user_id == telegram_id,
                    UsersBooksHistory.book_id == old_book_id,
                )
                .first()
            )
            assert old_book_history is not None
            assert old_book_history.end_read is None

    @mark.parametrize(
        "count_sentences, expected_status",
        [
            (1, status.HTTP_200_OK),
            (4, status.HTTP_200_OK),
            (5, status.HTTP_206_PARTIAL_CONTENT),
            (10, status.HTTP_206_PARTIAL_CONTENT),
        ],
    )
    def test_more_history_sentences(self, count_sentences, expected_status):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id
            users_history_book = (
                db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
            )
            assert users_history_book is None
            old_book = db.query(BooksModel).filter(BooksModel.level_en_id == telegram_user.level_en_id).first()
            old_book_id = old_book.book_id
            history_book = UsersBooksHistory(
                telegram_user_id=telegram_id,
                book_id=old_book.book_id,
                start_read=datetime.utcnow(),
            )
            db.add(history_book)
            for _ in range(count_sentences):
                sentence = (
                    db.query(BooksSentences)
                    .filter(BooksSentences.book_id == old_book_id)
                    .order_by(BooksSentences.order.asc())
                    .first()
                )
                history_book_sentence = UsersBooksSentencesHistory(
                    telegram_user_id=telegram_id,
                    sentence_id=sentence.sentence_id,
                    is_read=True,
                )
                db.add(history_book_sentence)
                db.commit()

        url = f"{self._url}/{telegram_id}/"
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == expected_status

    def test_get_same_sentence_if_not_read_sentence(self):

        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id
            users_history_book = (
                db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
            )
            assert users_history_book is None
            old_book = db.query(BooksModel).filter(BooksModel.level_en_id == telegram_user.level_en_id).first()
            old_book_id = old_book.book_id
            history_book = UsersBooksHistory(
                telegram_user_id=telegram_id,
                book_id=old_book.book_id,
                start_read=datetime.utcnow(),
            )
            db.add(history_book)
            first_sentence = (
                db.query(BooksSentences)
                .filter(BooksSentences.book_id == old_book_id)
                .order_by(BooksSentences.order.asc())
                .first()
            )
            first_sentence_id = first_sentence.sentence_id
            history_book_sentence = UsersBooksSentencesHistory(
                telegram_user_id=telegram_id,
                sentence_id=first_sentence_id,
                is_read=False,
                check_words=[],
            )
            db.add(history_book_sentence)
            db.commit()

        url = f"{self._url}/{telegram_id}/"
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()["detail"]

        with db_session() as db:
            assert old_book_id == response["book_id"]
            assert first_sentence_id == response["sentence_id"]
            users_history_book = (
                db.query(UsersBooksHistory)
                .filter(
                    UsersBooksHistory.telegram_user_id == telegram_id,
                    UsersBooksHistory.book_id == response["book_id"],
                )
                .first()
            )
            assert users_history_book is not None
            assert users_history_book.start_read is not None
            assert users_history_book.end_read is None
            users_history_book_sentence = db.query(UsersBooksSentencesHistory).filter(
                UsersBooksSentencesHistory.telegram_user_id == telegram_id,
                UsersBooksSentencesHistory.sentence_id == response["sentence_id"],
            )
            users_history_book_sentence = users_history_book_sentence.first()
            assert users_history_book_sentence is not None
            assert users_history_book_sentence.is_read is False
            assert users_history_book_sentence.sentence_id == response["sentence_id"]
            assert users_history_book_sentence.telegram_user_id == telegram_id
            assert users_history_book_sentence.id == response["history_sentence_id"]
            assert len(response["words"]) <= 5

    def test_not_get_read_without_headers(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id

        url = f"{self._url}/{telegram_id}/"
        response = self._client.get(url=url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_get_read_with_wrong_api_key_headers(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id

        url = f"{self._url}/{telegram_id}/"
        response = self._client.get(url=url, headers={"X-API-Key": "test"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
