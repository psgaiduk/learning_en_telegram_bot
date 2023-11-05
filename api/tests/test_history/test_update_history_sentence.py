from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import UsersBooksSentencesHistory
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
        response = self._client.patch(url=url, headers=self._headers, json=data_for_update)
        assert response.status_code == status.HTTP_200_OK
        
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

        expect_words = [11, 22, 34]
        assert check_words != expect_words

        data_for_update = {
            'id': history_sentence_id,
            'check_words': expect_words,
        }

        url = f'{self._url}/{history_sentence_id}/'
        response = self._client.patch(url=url, headers=self._headers, json=data_for_update)
        assert response.status_code == status.HTTP_200_OK

        with db_session() as db:
            history_sentence = db.query(UsersBooksSentencesHistory).filter(UsersBooksSentencesHistory.id == history_sentence_id).first()
            assert history_sentence.is_read is True
            assert history_sentence.id == history_sentence_id
            assert history_sentence.check_words == expect_words
            
    def test_update_check_words_and_is_read_history_sentence(self):
        """Test update check words and is_read history sentence."""

        with db_session() as db:
            history_sentence = db.query(UsersBooksSentencesHistory).first()
            history_sentence_id = history_sentence.id
            check_words = history_sentence.check_words
            assert history_sentence.is_read is True

        expect_words = [11, 22, 34]
        assert check_words != expect_words

        data_for_update = {
            'id': history_sentence_id,
            'check_words': expect_words,
            'is_read': False,
        }

        url = f'{self._url}/{history_sentence_id}/'
        response = self._client.patch(url=url, headers=self._headers, json=data_for_update)
        assert response.status_code == status.HTTP_200_OK

        with db_session() as db:
            history_sentence = db.query(UsersBooksSentencesHistory).filter(UsersBooksSentencesHistory.id == history_sentence_id).first()
            assert history_sentence.is_read is False
            assert history_sentence.id == history_sentence_id
            assert history_sentence.check_words == expect_words

    def test_not_update_without_check_words_and_is_read_history_sentence(self):
        """Test not update check words and is_read history sentence."""

        with db_session() as db:
            history_sentence = db.query(UsersBooksSentencesHistory).first()
            history_sentence_id = history_sentence.id

        data_for_update = {
            'id': history_sentence_id,
        }

        url = f'{self._url}/{history_sentence_id}/'
        response = self._client.patch(url=url, headers=self._headers, json=data_for_update)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_update_without_headers(self):
        """Test not update read history sentence without headers."""

        with db_session() as db:
            history_sentence = db.query(UsersBooksSentencesHistory).first()
            history_sentence_id = history_sentence.id

        data_for_update = {
            'id': history_sentence_id,
            'is_read': False,
        }

        url = f'{self._url}/{history_sentence_id}/'
        response = self._client.patch(url=url, json=data_for_update)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_update_with_wrong_api_key(self):
        """Test not update history sentence with wrong api key."""

        with db_session() as db:
            history_sentence = db.query(UsersBooksSentencesHistory).first()
            history_sentence_id = history_sentence.id

        data_for_update = {
            'id': history_sentence_id,
            'is_read': False,
        }

        url = f'{self._url}/{history_sentence_id}/'
        response = self._client.patch(url=url, json=data_for_update, headers={'X-API-Key': 'test'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

