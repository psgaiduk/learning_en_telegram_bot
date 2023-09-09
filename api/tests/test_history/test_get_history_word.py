from datetime import datetime
from random import choice, randint

from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import UsersWordsHistory, Words
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
    history_word_mock
)
from tests.connect_db import db_session


@mark.usefixtures('create_test_database', 'telegram_users_mock', 'history_word_mock')
class TestGetHistoryWordAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)
        cls._url = '/api/v1/history/words'

    def test_get_word_history(self):
        with db_session() as db:
            history_word = db.query(UsersWordsHistory).first()

        url = f'{self._url}/{history_word.telegram_user_id}/'
        response = self._client.get(url=url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()

        assert response['total'] == 1
        assert response['results'][0]['telegram_user_id'] == history_word.telegram_user_id
        assert response['results'][0]['word_id'] == history_word.word_id
        assert response['results'][0]['is_known'] == history_word.is_known
        assert response['results'][0]['count_view'] == history_word.count_view
        assert response['results'][0]['correct_answers'] == history_word.correct_answers
        assert response['results'][0]['incorrect_answers'] == history_word.incorrect_answers
        assert response['results'][0]['correct_answers_in_row'] == history_word.correct_answers_in_row
        assert response['results'][0]['created_at'] == history_word.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        assert response['results'][0]['updated_at'] == history_word.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f')

