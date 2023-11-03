from datetime import datetime

from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import BooksModel, Users, UsersBooksHistory, UsersBooksSentencesHistory, BooksSentences
from settings import settings
from tests.fixtures import (
    create_test_database,
    telegram_users_mock,
    book_mock,
    history_book_not_complete_mock,
    level_en_mock,
    main_language_mock,
    hero_level_mock,
    type_words_mock,
    book_sentences_mock,
    words_mock,
)
from tests.connect_db import db_session


@mark.usefixtures('create_test_database', 'telegram_users_mock', 'book_mock', 'book_sentences_mock', 'words_mock')
class TestReadApi:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)
        cls._url = '/api/v1/read'

    def test_get_first_sentence_for_not_read_early(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id
            users_history_book = db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
            assert users_history_book is None
            users_history_book_sentence = (
                db.query(UsersBooksSentencesHistory)
                .filter(UsersBooksSentencesHistory.telegram_user_id == telegram_id)
                .first()
            )
            assert users_history_book_sentence is None

        url = f'{self._url}/{telegram_id}/'
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()['detail']

        with db_session() as db:
            users_history_book = db.query(UsersBooksHistory).filter(UsersBooksHistory.telegram_user_id == telegram_id).first()
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
            assert users_history_book_sentence.is_read is False
            assert users_history_book_sentence.sentence_id == response['sentence_id']
            assert users_history_book_sentence.telegram_user_id == telegram_id
            book = db.query(BooksModel).filter(BooksModel.book_id == book_id).first()
            assert f'{book.author} - {book.title}' in response['text']
            assert len(response['words']) <= 5
            sentence = db.query(BooksSentences).filter(BooksSentences.sentence_id == response['sentence_id']).first()
            assert sentence.order == 1
