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

        data_for_create = {
            'telegram_user_id': telegram_user.telegram_id,
            'word_id': word.word_id,
        }

        url = f'{self._url}/'
        response = self._client.post(url=url, headers=self._headers, json=data_for_create)
        assert response.status_code == status.HTTP_201_CREATED
        response = response.json()

        with db_session() as db:
            words_history = db.query(UsersWordsHistory).filter(
                UsersWordsHistory.telegram_user_id == telegram_user.telegram_id,
                UsersWordsHistory.word_id == word.word_id,
            ).first()
            assert words_history.id == response['detail']['id']
            assert words_history.telegram_user_id == response['detail']['telegram_user_id'] == telegram_user.telegram_id
            assert words_history.word_id == response['detail']['word_id'] == word.word_id
            assert words_history.word.word == response['detail']['word'] == word.word
            assert words_history.word.translation == response['detail']['translation'] == word.translation
            assert words_history.word.type_word_id == response['detail']['type_word_id'] == word.type_word_id
            assert words_history.is_known == response['detail']['is_known'] is False
            assert words_history.count_view == response['detail']['count_view'] == 0
            assert words_history.correct_answers == response['detail']['correct_answers'] == 0
            assert words_history.incorrect_answers == response['detail']['incorrect_answers'] == 0
            assert words_history.correct_answers_in_row == response['detail']['correct_answers_in_row'] == 0
            assert words_history.created_at == datetime.strptime(response['detail']['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            assert words_history.updated_at == datetime.strptime(response['detail']['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')

    def test_not_create_history_word_without_api_key(self):
        with db_session() as db:
            word = db.query(Words).first()
            telegram_user = db.query(Users).first()
            
        data_for_create = {
            'telegram_user_id': telegram_user.telegram_id,
            'word_id': word.word_id,
        }

        url = f'{self._url}/'
        response = self._client.post(url=url, json=data_for_create)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_create_history_word_with_wrong_api_key(self):
        with db_session() as db:
            word = db.query(Words).first()
            telegram_user = db.query(Users).first()
            
        data_for_create = {
            'telegram_user_id': telegram_user.telegram_id,
            'word_id': word.word_id,
        }

        url = f'{self._url}/'
        response = self._client.post(url=url, headers={'X-API-Key': 'wrong_api_key'}, json=data_for_create)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_create_history_word_with_wrong_word_id(self):
        with db_session() as db:
            word = db.query(Words).order_by(Words.word_id.desc()).first()
            word_id = word.word_id + 1
            telegram_user = db.query(Users).first()

        data_for_create = {
            'telegram_user_id': telegram_user.telegram_id,
            'word_id': word_id,
        }

        url = f'{self._url}/'
        response = self._client.post(url=url, headers=self._headers, json=data_for_create)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_not_create_history_word_without_word_id(self):
        with db_session() as db:
            telegram_user = db.query(Users).first()

        data_for_create = {
            'telegram_user_id': telegram_user.telegram_id,
        }

        url = f'{self._url}/'
        response = self._client.post(url=url, headers=self._headers, json=data_for_create)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_not_create_history_word_with_wrong_user_id(self):
        with db_session() as db:
            word = db.query(Words).first()
            telegram_user = db.query(Users).order_by(Users.telegram_id).first()
            telegram_user_id = telegram_user.telegram_id + 1

        data_for_create = {
            'telegram_user_id': telegram_user_id,
            'word_id': word.word_id,
        }

        url = f'{self._url}/'
        response = self._client.post(url=url, headers=self._headers, json=data_for_create)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_not_create_history_word_without_user_id(self):
        with db_session() as db:
            word = db.query(Words).first()

        data_for_create = {
            'word_id': word.word_id,
        }

        url = f'{self._url}/'
        response = self._client.post(url=url, headers=self._headers, json=data_for_create)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_not_create_word_history_again(self):
        with db_session() as db:
            word = db.query(Words).first()
            telegram_user = db.query(Users).first()

        data_for_create = {
            'telegram_user_id': telegram_user.telegram_id,
            'word_id': word.word_id,
        }

        url = f'{self._url}/'
        response = self._client.post(url=url, headers=self._headers, json=data_for_create)
        assert response.status_code == status.HTTP_201_CREATED

        url = f'{self._url}/'
        response = self._client.post(url=url, headers=self._headers, json=data_for_create)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
