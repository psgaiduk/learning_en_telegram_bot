from datetime import datetime

from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import Words, Users, UsersWordsHistory
from settings import settings
from tests.fixtures import (
    create_test_database,
    telegram_users_mock,
    words_mock,
    book_mock,
    book_sentences_mock,
    type_words_mock,
    level_en_mock,
    main_language_mock,
    hero_level_mock,
)
from tests.connect_db import db_session


@mark.usefixtures('create_test_database', 'telegram_users_mock', 'words_mock')
class TestCreateHistoryWordAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)
        cls._url = '/api/v1/history/words'

    def test_create_word_history(self):
        with db_session() as db:
            word = db.query(Words).first()
            telegram_user = db.query(Users).first()

        url = f'{self._url}/{telegram_user.telegram_id}/{word.word_id}/'
        response = self._client.post(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_201_CREATED
        response = response.json()

        with db_session() as db:
            words_history = db.query(UsersWordsHistory).filter(
                UsersWordsHistory.telegram_user_id == telegram_user.telegram_id,
                UsersWordsHistory.word_id == word.word_id,
            ).first()
            assert words_history.id == response['id']
            assert words_history.telegram_user_id == response['telegram_user_id'] == telegram_user.telegram_id
            assert words_history.word_id == response['word_id'] == word.word_id
            assert words_history.is_known == response['is_known'] is False
            assert words_history.count_view == response['count_view'] == 0
            assert words_history.correct_answers == response['correct_answers'] == 0
            assert words_history.incorrect_answers == response['incorrect_answers'] == 0
            assert words_history.correct_answers_in_row == response['correct_answers_in_row'] == 0
            assert words_history.created_at == datetime.strptime(response['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            assert words_history.updated_at == datetime.strptime(response['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')

    def test_not_create_history_word_without_api_key(self):
        with db_session() as db:
            word = db.query(Words).first()
            telegram_user = db.query(Users).first()

        url = f'{self._url}/{telegram_user.telegram_id}/{word.word_id}/'
        response = self._client.post(url=url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_create_history_word_with_wrong_api_key(self):
        with db_session() as db:
            word = db.query(Words).first()
            telegram_user = db.query(Users).first()

        url = f'{self._url}/{telegram_user.telegram_id}/{word.word_id}/'
        response = self._client.post(url=url, headers={'X-API-Key': 'wrong_api_key'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_create_history_word_with_wrong_book_id(self):
        with db_session() as db:
            word = db.query(Words).order_by(Words.word_id.desc()).first()
            word_id = word.word_id + 1
            telegram_user = db.query(Users).first()

        url = f'{self._url}/{telegram_user.telegram_id}/{word_id}/'
        response = self._client.post(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
    def test_not_create_history_word_with_wrong_user_id(self):
        with db_session() as db:
            word = db.query(Words).first()
            telegram_user = db.query(Users).order_by(Users.telegram_id).first()
            telegram_user_id = telegram_user.telegram_id - 1

        url = f'{self._url}/{telegram_user_id}/{word.word_id}/'
        response = self._client.post(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
