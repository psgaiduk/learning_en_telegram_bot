from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import UsersWordsHistory
from settings import settings
from tests.connect_db import db_session

from tests.fixtures import *


@mark.usefixtures('create_test_database', 'history_word_mock')
class TestUpdateHistoryWordAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)
        cls._url = '/api/v1/history/words'

    def test_update_word_history(self):
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
