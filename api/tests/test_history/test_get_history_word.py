from math import ceil

from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import UsersWordsHistory
from settings import settings
from tests.connect_db import db_session

from tests.fixtures import *


@mark.usefixtures('create_test_database')
class TestGetHistoryWordAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)
        cls._url = '/api/v1/history/words'

    def test_get_word_history(self, history_word_mock):
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

    def test_get_word_history_pagination(self, history_all_words_mock):

        with db_session() as db:
            telegram_user_id = db.query(UsersWordsHistory).first().telegram_user_id

            limit = 100
            page = 1
            
            history_user_words_query = db.query(UsersWordsHistory).filter(
                UsersWordsHistory.telegram_user_id == telegram_user_id
            )

            url = f'{self._url}/{telegram_user_id}/'
            response = self._client.get(url=url, headers=self._headers)
            assert response.status_code == status.HTTP_200_OK
            response = response.json()

            history_user_words = history_user_words_query.all()

            total_count = len(history_user_words)
            total_pages = ceil(total_count / limit)
            per_page = total_count - (limit * (page - 1))
            if per_page > limit:
                per_page = limit

            assert response['total'] == total_count
            assert response['total_pages'] == total_pages
            assert response['per_page'] == per_page
            assert response['page'] == page

            page = 2
            params_for_get_history_words = {
                'page': page,
            }

            per_page = total_count - (limit * (page - 1))
            if per_page > limit:
                per_page = limit

            url = f'{self._url}/{telegram_user_id}/'
            response = self._client.get(url=url, headers=self._headers, params=params_for_get_history_words)
            assert response.status_code == status.HTTP_200_OK
            response = response.json()

            assert response['total'] == total_count
            assert response['total_pages'] == total_pages
            assert response['per_page'] == per_page
            assert response['page'] == page

            page = 3
            limit = 10

            total_pages = ceil(total_count / limit)
            per_page = total_count - (limit * (page - 1))
            if per_page > limit:
                per_page = limit

            params_for_get_history_words = {
                'page': page,
                'limit': limit,
            }

            url = f'{self._url}/{telegram_user_id}/'
            response = self._client.get(url=url, headers=self._headers, params=params_for_get_history_words)
            assert response.status_code == status.HTTP_200_OK
            response = response.json()

            assert response['total'] == total_count
            assert response['total_pages'] == total_pages
            assert response['per_page'] == per_page
            assert response['page'] == page

    def test_get_word_history_filter_is_known(self, history_all_words_mock):

        with db_session() as db:
            telegram_user_id = db.query(UsersWordsHistory).first().telegram_user_id
            total_from_db = 0
            for test_value in (True, False):
                history_user_words = db.query(UsersWordsHistory).filter(
                    UsersWordsHistory.telegram_user_id == telegram_user_id,
                    UsersWordsHistory.is_known == test_value,
                ).all()

                response_total = self._send_request_and_get_response_total(
                    telegram_user_id=telegram_user_id,
                    params_for_get_history_words={'is_known': test_value},
                )

                assert response_total == len(history_user_words)
                total_from_db += len(history_user_words)

            all_history_user_words_query = db.query(UsersWordsHistory).filter(
                UsersWordsHistory.telegram_user_id == telegram_user_id
            ).all()
            assert len(all_history_user_words_query) == total_from_db

    def _send_request_and_get_response_total(self, telegram_user_id, params_for_get_history_words):
        url = f'{self._url}/{telegram_user_id}/'
        response = self._client.get(url=url, headers=self._headers, params=params_for_get_history_words)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        return response['total']

    def test_get_word_history_filter_count_view(self, history_all_words_mock):

        with db_session() as db:
            telegram_user_id = db.query(UsersWordsHistory).first().telegram_user_id

            history_user_words_gte = db.query(UsersWordsHistory).filter(
                UsersWordsHistory.telegram_user_id == telegram_user_id,
                UsersWordsHistory.count_view >= 10,
            ).all()

            params_for_get_history_words = {
                'count_view_gte': 10,
            }

            url = f'{self._url}/{telegram_user_id}/'
            response = self._client.get(url=url, headers=self._headers, params=params_for_get_history_words)
            assert response.status_code == status.HTTP_200_OK
            response = response.json()

            assert response['total'] == len(history_user_words_gte)

            history_user_words_lte = db.query(UsersWordsHistory).filter(
                UsersWordsHistory.telegram_user_id == telegram_user_id,
                UsersWordsHistory.count_view <= 9,
            ).all()

            params_for_get_history_words = {
                'count_view_lte': 9,
            }

            url = f'{self._url}/{telegram_user_id}/'
            response = self._client.get(url=url, headers=self._headers, params=params_for_get_history_words)
            assert response.status_code == status.HTTP_200_OK
            response = response.json()

            assert response['total'] == len(history_user_words_lte)

            all_history_user_words_query = db.query(UsersWordsHistory).filter(
                UsersWordsHistory.telegram_user_id == telegram_user_id,
            ).all()

            assert len(all_history_user_words_query) == len(history_user_words_gte) + len(history_user_words_lte)

    def test_get_word_history_filter_word_id(self, history_all_words_mock):

        with db_session() as db:
            word_history_for_user = db.query(UsersWordsHistory).first()
            telegram_user_id = word_history_for_user.telegram_user_id
            word_id = word_history_for_user.word_id

            params_for_get_history_words = {
                'word_id': word_id,
            }

            url = f'{self._url}/{telegram_user_id}/'
            response = self._client.get(url=url, headers=self._headers, params=params_for_get_history_words)
            assert response.status_code == status.HTTP_200_OK
            response = response.json()

            assert response['total'] == 1
