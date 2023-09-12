from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import Users, UsersWordsHistory, Words
from settings import settings
from tests.connect_db import db_session

from tests.fixtures import *


@mark.usefixtures('create_test_database')
class TestUpdateHistoryWordAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)
        cls._url = '/api/v1/history/words'

    def test_update_word_history(self, history_word_mock):
        with db_session() as db:
            history_word = db.query(UsersWordsHistory).first()

        url = f'{self._url}/'

        assert history_word.is_known is False
        assert history_word.count_view == 0
        assert history_word.correct_answers == 0
        assert history_word.incorrect_answers == 0
        assert history_word.correct_answers_in_row == 0

        params_for_update = {
            'telegram_user_id': history_word.telegram_user_id,
            'word_id': history_word.word_id,
            'is_known': True,
            'count_view': 1,
            'correct_answers': 1,
            'incorrect_answers': 1,
            'correct_answers_in_row': 1,
        }

        response = self._client.patch(url=url, headers=self._headers, json=params_for_update)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()

        with db_session() as db:
            history_word = db.query(UsersWordsHistory).first()

        assert response['detail']['telegram_user_id'] == history_word.telegram_user_id
        assert response['detail']['word_id'] == history_word.word_id
        assert response['detail']['is_known'] == history_word.is_known is True
        assert response['detail']['count_view'] == history_word.count_view == 1
        assert response['detail']['correct_answers'] == history_word.correct_answers == 1
        assert response['detail']['incorrect_answers'] == history_word.incorrect_answers == 1
        assert response['detail']['correct_answers_in_row'] == history_word.correct_answers_in_row == 1
        assert response['detail']['created_at'] == history_word.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        assert response['detail']['updated_at'] == history_word.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f')

    @mark.parametrize('name_field, value_field', [
        ('is_known', True),
        ('count_view', 1),
        ('correct_answers', 1),
        ('incorrect_answers', 1),
        ('correct_answers_in_row', 1),
    ])
    def test_update_word_history_by_one_value(self, name_field, value_field, history_word_mock):

        with db_session() as db:
            history_word = db.query(UsersWordsHistory).first()

        url = f'{self._url}/'

        params_for_update = {
            'telegram_user_id': history_word.telegram_user_id,
            'word_id': history_word.word_id,
            name_field: value_field,
        }

        response = self._client.patch(url=url, headers=self._headers, json=params_for_update)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()

        assert response['detail'][name_field] == value_field

    @mark.parametrize('name_field, value_field', [
        ('telegram_user_id', 1),
        ('word_id', 1),
    ])
    def test_not_update_without_required_fields(self, name_field, value_field, history_word_mock):

        url = f'{self._url}/'

        params_for_update = {
            name_field: value_field,
            'is_known': True,
            'count_view': 1,
            'correct_answers': 1,
            'incorrect_answers': 1,
            'correct_answers_in_row': 1,
        }

        response = self._client.patch(url=url, headers=self._headers, json=params_for_update)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_not_update_word_history_with_wrong_telegram_id(self, history_word_mock):
        with db_session() as db:
            telegram_id = db.query(Users).order_by(Users.telegram_id.desc()).first().telegram_id + 1
            word_id = db.query(Words).order_by(Words.word_id).first().word_id

        url = f'{self._url}/'

        params_for_update = {
            'telegram_user_id': telegram_id,
            'word_id': word_id,
            'is_known': True,
            'count_view': 1,
            'correct_answers': 1,
            'incorrect_answers': 1,
            'correct_answers_in_row': 1,
        }

        response = self._client.patch(url=url, headers=self._headers, json=params_for_update)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_not_update_word_history_with_wrong_word_id(self, history_word_mock):
        with db_session() as db:
            telegram_id = db.query(Users).order_by(Users.telegram_id).first().telegram_id
            word_id = db.query(Words).order_by(Words.word_id.desc()).first().word_id + 1

        url = f'{self._url}/'

        params_for_update = {
            'telegram_user_id': telegram_id,
            'word_id': word_id,
            'is_known': True,
            'count_view': 1,
            'correct_answers': 1,
            'incorrect_answers': 1,
            'correct_answers_in_row': 1,
        }

        response = self._client.patch(url=url, headers=self._headers, json=params_for_update)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_not_update_word_history_without_history_word(self, telegram_users_mock, words_mock):
        with db_session() as db:
            telegram_id = db.query(Users).order_by(Users.telegram_id).first().telegram_id
            word_id = db.query(Words).order_by(Words.word_id).first().word_id

        url = f'{self._url}/'

        params_for_update = {
            'telegram_user_id': telegram_id,
            'word_id': word_id,
            'is_known': True,
            'count_view': 1,
            'correct_answers': 1,
            'incorrect_answers': 1,
            'correct_answers_in_row': 1,
        }

        response = self._client.patch(url=url, headers=self._headers, json=params_for_update)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_update_word_history_without_api_key(self, history_word_mock):
        with db_session() as db:
            history_word = db.query(UsersWordsHistory).first()

        url = f'{self._url}/'

        params_for_update = {
            'telegram_user_id': history_word.telegram_user_id,
            'word_id': history_word.word_id,
            'is_known': True,
            'count_view': 1,
            'correct_answers': 1,
            'incorrect_answers': 1,
            'correct_answers_in_row': 1,
        }

        response = self._client.patch(url=url, json=params_for_update)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_update_word_history_with_wrong_api_key(self, history_word_mock):
        with db_session() as db:
            history_word = db.query(UsersWordsHistory).first()

        url = f'{self._url}/'

        params_for_update = {
            'telegram_user_id': history_word.telegram_user_id,
            'word_id': history_word.word_id,
            'is_known': True,
            'count_view': 1,
            'correct_answers': 1,
            'incorrect_answers': 1,
            'correct_answers_in_row': 1,
        }

        response = self._client.patch(url=url, json=params_for_update, headers={'X-API-Key': 'test'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
