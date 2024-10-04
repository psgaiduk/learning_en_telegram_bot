from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import joinedload
from fastapi import status
from pytest import fail, mark

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
    tenses_mock,
)
from models import BooksModel, BooksSentences
from settings import settings


@mark.usefixtures("create_test_database", "book_mock")
class TestGetBookAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {"X-API-Key": settings.api_key}
        cls._client = TestClient(app)

    def test_good_get_book_by_id(self, book_sentences_mock, words_mock):
        with db_session() as db:
            first_book = (
                db.query(BooksModel)
                .options(joinedload(BooksModel.books_sentences).joinedload(BooksSentences.words))
                .order_by(BooksSentences.order)
                .first()
            )

            if not first_book:
                fail("Test data is not initialized properly.")

            response = self._client.get(f"/api/v1/books/{first_book.book_id}/", headers=self._headers)
            assert response.status_code == status.HTTP_200_OK

            response = response.json()
            assert response["title"] == first_book.title
            assert response["author"] == first_book.author
            assert response["level_en_id"] == first_book.level_en_id

            book_first_sentence = response["books_sentences"][0]

            assert len(response["books_sentences"]) == len(first_book.books_sentences)
            assert book_first_sentence["text"] == first_book.books_sentences[0].text
            assert book_first_sentence["translation"] == first_book.books_sentences[0].translation

            assert len(book_first_sentence["words"]) == len(first_book.books_sentences[0].words)
            assert book_first_sentence["words"][0]["word"] == first_book.books_sentences[0].words[0].word
            assert book_first_sentence["words"][0]["translation"] == first_book.books_sentences[0].words[0].translation

    def test_not_found_get_book_by_id(self):
        with db_session() as db:
            last_book = db.query(BooksModel).order_by(BooksModel.book_id.desc()).first()

            if not last_book:
                fail("Test data is not initialized properly.")

            response = self._client.get(f"/api/v1/books/{last_book.book_id + 1}/", headers=self._headers)
            assert response.status_code == 404

    def test_not_get_book_without_api_key(self, book_sentences_mock, words_mock):
        with db_session() as db:
            first_book = (
                db.query(BooksModel)
                .options(joinedload(BooksModel.books_sentences).joinedload(BooksSentences.words))
                .order_by(BooksSentences.order)
                .first()
            )

            if not first_book:
                fail("Test data is not initialized properly.")

            response = self._client.get(f"/api/v1/books/{first_book.book_id}/")
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
