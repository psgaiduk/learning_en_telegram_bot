from datetime import datetime

from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import BooksSentences, Users, UsersBooksSentencesHistory, UsersWordsHistory
from settings import settings
from tests.connect_db import db_session

from tests.fixtures import *


@mark.usefixtures('create_test_database', 'telegram_users_mock', 'words_mock', 'book_mock', 'book_sentences_mock')
class TestCreateHistorySentenceAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)
        cls._url = '/api/v1/history/sentences'

    def test_create_sentence_history(self):
        with db_session() as db:
            sentence = db.query(BooksSentences).first()
            telegram_user = db.query(Users).first()

        data_for_create = {
            'telegram_id': telegram_user.telegram_id,
            'sentence_id': sentence.sentence_id,
        }

        url = f'{self._url}/'
        response = self._client.post(url=url, headers=self._headers, json=data_for_create)
        assert response.status_code == status.HTTP_201_CREATED
        response = response.json()

        with db_session() as db:
            sentence_history = db.query(UsersBooksSentencesHistory).filter(
                UsersBooksSentencesHistory.telegram_id == telegram_user.telegram_id,
                UsersBooksSentencesHistory.sentence_id == sentence.sentence_id,
            ).first()
            assert sentence_history.id == response['detail']['id']
            assert sentence_history.telegram_id == response['detail']['telegram_id'] == telegram_user.telegram_id
            assert sentence_history.sentence_id == response['detail']['sentence_id'] == sentence.sentence_id
            assert sentence_history.is_read == response['detail']['is_read'] is False
            assert sentence_history.created_at == datetime.fromisoformat(response['detail']['created_at'])
            assert response['detail']['words'] is not None
            for word in response['detail']['words']:
                assert word['id'] is None
                assert word['word_id'] is not None
                assert word['word'] is not None
                assert word['type_word_id'] is not None
                assert word['translation'] is not None
                assert word['is_known'] is None
                assert word['count_view'] is None
                assert word['correct_answers'] is None
                assert word['incorrect_answers'] is None
                assert word['correct_answers_in_row'] is None
                assert word['created_at'] is None
                assert word['updated_at'] is None

                history_book = UsersWordsHistory(
                    telegram_user_id=telegram_user.telegram_id,
                    word_id=word['word_id'],
                    is_known=False,
                    count_view=3,
                    correct_answers=2,
                    incorrect_answers=1,
                    correct_answers_in_row=0,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )

                db.add(history_book)

            db.delete(sentence_history)
            db.commit()

        response = self._client.post(url=url, headers=self._headers, json=data_for_create)
        assert response.status_code == status.HTTP_201_CREATED
        response = response.json()

        with db_session() as db:
            sentence_history = db.query(UsersBooksSentencesHistory).filter(
                UsersBooksSentencesHistory.telegram_id == telegram_user.telegram_id,
                UsersBooksSentencesHistory.sentence_id == sentence.sentence_id,
            ).first()
            assert sentence_history.id == response['detail']['id']
            assert sentence_history.telegram_id == response['detail']['telegram_id'] == telegram_user.telegram_id
            assert sentence_history.sentence_id == response['detail']['sentence_id'] == sentence.sentence_id
            assert sentence_history.is_read == response['detail']['is_read'] is False
            assert sentence_history.created_at == datetime.fromisoformat(response['detail']['created_at'])
            assert response['detail']['words'] is not None
            for word in response['detail']['words']:
                assert word['id'] is not None
                assert word['word_id'] is not None
                assert word['word'] is not None
                assert word['type_word_id'] is not None
                assert word['translation'] is not None
                assert word['is_known'] is not None
                assert word['count_view'] == 3
                assert word['correct_answers'] == 2
                assert word['incorrect_answers'] == 1
                assert word['correct_answers_in_row'] == 0
                assert word['created_at'] is not None
                assert word['updated_at'] is not None

    def test_not_create_sentence_history_with_wrong_telegram_id(self):
        with db_session() as db:
            sentence = db.query(BooksSentences).first()
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_id = telegram_user.telegram_id + 1

        data_for_create = {
            'telegram_id': telegram_id,
            'sentence_id': sentence.sentence_id,
        }

        url = f'{self._url}/'
        response = self._client.post(url=url, headers=self._headers, json=data_for_create)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_not_create_sentence_history_with_wrong_sentence_id(self):
        with db_session() as db:
            sentence = db.query(BooksSentences).order_by(BooksSentences.sentence_id.desc()).first()
            telegram_user = db.query(Users).first()
            sentence_id = sentence.sentence_id + 1

        data_for_create = {
            'telegram_id': telegram_user.telegram_id,
            'sentence_id': sentence_id,
        }

        url = f'{self._url}/'
        response = self._client.post(url=url, headers=self._headers, json=data_for_create)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_not_create_sentence_history_again(self):
        with db_session() as db:
            sentence = db.query(BooksSentences).first()
            telegram_user = db.query(Users).first()

        data_for_create = {
            'telegram_id': telegram_user.telegram_id,
            'sentence_id': sentence.sentence_id,
        }

        url = f'{self._url}/'
        response = self._client.post(url=url, headers=self._headers, json=data_for_create)
        assert response.status_code == status.HTTP_201_CREATED

        response = self._client.post(url=url, headers=self._headers, json=data_for_create)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_create_sentence_history_without_api_key(self):
        with db_session() as db:
            sentence = db.query(BooksSentences).first()
            telegram_user = db.query(Users).first()

        data_for_create = {
            'telegram_id': telegram_user.telegram_id,
            'sentence_id': sentence.sentence_id,
        }

        url = f'{self._url}/'
        response = self._client.post(url=url, json=data_for_create)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_create_sentence_history_with_wrong_api_key(self):
        with db_session() as db:
            sentence = db.query(BooksSentences).first()
            telegram_user = db.query(Users).first()

        data_for_create = {
            'telegram_id': telegram_user.telegram_id,
            'sentence_id': sentence.sentence_id,
        }

        url = f'{self._url}/'
        response = self._client.post(url=url, json=data_for_create, headers={'X-API-Key': 'test'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
