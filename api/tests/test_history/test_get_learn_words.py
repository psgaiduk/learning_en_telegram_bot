from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import UsersWordsHistory
from settings import settings
from tests.connect_db import db_session

from tests.fixtures import *


@mark.usefixtures('create_test_database')
class TestGetLearnWordsAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)
        cls._url = '/api/v1/history/learn-words'

    def test_get_learn_words(self, history_word_mock):
        with db_session() as db:
            history_word = db.query(UsersWordsHistory).first()
            history_word.is_known = True
            db.commit()
            telegram_id = history_word.telegram_user_id

        url = f'{self._url}/{telegram_id}/'
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()

        assert len(response) == 1
        assert response[0]['repeat_datetime'] < datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

    def test_get_learn_words_with_bad_repeat_datetime(self, history_word_mock):
        with db_session() as db:
            history_word: UsersWordsHistory = db.query(UsersWordsHistory).first()
            history_word.is_known = True
            history_word.repeat_datetime = datetime.utcnow() + timedelta(hours=4)
            db.commit()
            telegram_id = history_word.telegram_user_id

        url = f'{self._url}/{telegram_id}/'
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()

        assert len(response) == 0

    def test_not_get_learn_words_with_is_false_known(self, history_word_mock):
        with db_session() as db:
            history_word: UsersWordsHistory = db.query(UsersWordsHistory).first()
            assert history_word
            assert history_word.is_known is False
            telegram_id = history_word.telegram_user_id

        url = f'{self._url}/{telegram_id}/'
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()

        assert len(response) == 0
