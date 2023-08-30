from datetime import datetime

from fastapi.testclient import TestClient
from main import app
from fastapi import status
import pytest

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
from models import BooksModel, BooksSentences, Words, sentence_word_association, Users, UsersBooksHistory
from settings import settings


class TestBookAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)

    def test_good_get_book_by_id(self, create_test_database, book_mock, book_sentences_mock, words_mock):
        with db_session() as db:
            first_book = (
                db.query(BooksModel)
                .join(BooksSentences, BooksModel.book_id == BooksSentences.book_id)
                .join(sentence_word_association)
                .join(Words)
                .order_by(BooksModel.book_id, BooksSentences.order)
                .first()
            )

            if not first_book:
                pytest.fail('Test data is not initialized properly.')

            response = self._client.get(f'/api/v1/books/{first_book.book_id}/', headers=self._headers)
            assert response.status_code == status.HTTP_200_OK

            response = response.json()
            assert response['title'] == first_book.title
            assert response['author'] == first_book.author

            book_first_sentence = response['books_sentences'][0]
            assert len(response['books_sentences']) == len(first_book.books_sentences)
            assert book_first_sentence['text'] == first_book.books_sentences[0].text
            assert book_first_sentence['translation'] == first_book.books_sentences[0].translation

            assert len(book_first_sentence['words']) == len(first_book.books_sentences[0].words)
            assert book_first_sentence['words'][0]['word'] == first_book.books_sentences[0].words[0].word
            assert book_first_sentence['words'][0]['translation'] == first_book.books_sentences[0].words[0].translation

    def test_not_found_get_book_by_id(self, create_test_database, book_mock):
        with db_session() as db:
            last_book = db.query(BooksModel).order_by(BooksModel.book_id.desc()).first()

            if not last_book:
                pytest.fail('Test data is not initialized properly.')

            response = self._client.get(f'/api/v1/books/{last_book.book_id + 1}/', headers=self._headers)
            assert response.status_code == 404
    
    def test_good_get_random_book_for_user(self, create_test_database, book_mock, telegram_users_mock):
        with db_session() as db:
            user = db.query(Users).first()

            if not user:
                pytest.fail('Test data is not initialized properly.')

            response = self._client.get(f'/api/v1/books/get-random-book/{user.telegram_id}/', headers=self._headers)
            assert response.status_code == status.HTTP_200_OK

            response = response.json()
            assert response['level_en_id'] == user.level_en_id

    def test_not_found_get_random_book_for_user(self, create_test_database, book_mock, telegram_users_mock):
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
