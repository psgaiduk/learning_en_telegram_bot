from fastapi.testclient import TestClient
from main import app
from fastapi import status
import pytest

from tests.connect_db import db_session
from tests.fixtures import book_mock, create_test_database, level_en_mock, book_sentences_mock
from models import BooksModel
from settings import settings


class TestBookAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)

    def test_good_get_book_by_id(self, create_test_database, book_mock, book_sentences_mock):
        with db_session() as db:
            first_book = db.query(BooksModel).first()

            if not first_book:
                pytest.fail('Test data is not initialized properly.')

            response = self._client.get(f'/api/v1/books/{first_book.book_id}/', headers=self._headers)
            assert response.status_code == status.HTTP_200_OK
            assert response.json()['title'] == first_book.title
            assert response.json()['author'] == first_book.author
            assert len(response.json()['books_sentences']) == len(first_book.books_sentences)

    def test_not_found_get_book_by_id(self, create_test_database, book_mock):
        with db_session() as db:
            last_book = db.query(BooksModel).order_by(BooksModel.book_id.desc()).first()

            if not last_book:
                pytest.fail('Test data is not initialized properly.')

            response = self._client.get(f'/api/v1/books/{last_book.book_id + 1}/', headers=self._headers)
            assert response.status_code == 404
