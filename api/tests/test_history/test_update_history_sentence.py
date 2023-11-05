from datetime import datetime

from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import Users, UsersBooksSentencesHistory
from settings import settings
from tests.connect_db import db_session

from tests.fixtures import *


@mark.usefixtures('create_test_database', 'history_book_sentence_complete_mock')
class TestUpdateHistorySentenceAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)
        cls._url = '/api/v1/history/sentences'

    def test_update_is_read_history_sentence(self):
        """Test update is read history sentence."""

        with db_session() as db:
            history_sentence = db.query(UsersBooksSentencesHistory).first()
            history_sentence_id = history_sentence.id
            assert history_sentence.is_read is True

        data_for_update = {
            'id': history_sentence_id,
            'is_read': False,
        }

        url = f'{self._url}/{history_sentence_id}/'
        response = self._client.post(url=url, headers=self._headers, json=data_for_update)
        assert response.status_code == status.HTTP_200_CREATED
        
        with db_session() as db:
            history_sentence = db.query(UsersBooksSentencesHistory).filter(UsersBooksSentencesHistory.id==history_sentence_id).first()
            assert history_sentence.is_read is False
            assert history_sentence.id == history_sentence_id

    def test_update_check_words_history_sentence(self):
        """Test update check words history sentence."""

        with db_session() as db:
            history_sentence = db.query(UsersBooksSentencesHistory).first()
            history_sentence_id = history_sentence.id
            check_words = history_sentence.check_words
            assert history_sentence.is_read is True

        expect_words = [1, 2, 3]
        assert check_words != expect_words

        data_for_update = {
            'id': history_sentence_id,
            'check_words': expect_words,
        }

        url = f'{self._url}/{history_sentence_id}/'
        response = self._client.post(url=url, headers=self._headers, json=data_for_update)
        assert response.status_code == status.HTTP_200_CREATED

        with db_session() as db:
            history_sentence = db.query(UsersBooksSentencesHistory).filter(UsersBooksSentencesHistory.id == history_sentence_id).first()
            assert history_sentence.is_read is True
            assert history_sentence.id == history_sentence_id
            assert history_sentence.check_words == expect_words

