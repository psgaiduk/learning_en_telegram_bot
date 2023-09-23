from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import Users, UsersWordsHistory, Words
from settings import settings
from tests.connect_db import db_session

from tests.fixtures import *


@mark.usefixtures('create_test_database', 'telegram_users_mock')
class TestCreateReferralAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)
        cls._url = '/api/v1/referrals/'

    def test_create_referral_user(self):
        with db_session() as db:
            telegram_users = db.query(Users).all()
            first_telegram_user = telegram_users[0]
            second_telegram_user = telegram_users[1]
            third_telegram_user = telegram_users[2]

        data_for_create_referral = {
            'telegram_user_id': first_telegram_user.telegram_id,
            'friend_telegram_id': second_telegram_user.telegram_id,
        }
        print(data_for_create_referral)

        response = self._client.post(url=self._url, headers=self._headers, json=data_for_create_referral)
        assert response.status_code == status.HTTP_201_CREATED
        # response = response.json()
        # assert response['detail']['telegram_id'] == first_telegram_user.telegram_id
        # print(response['detail']['telegram_id'])
        # print(response['detail']['friends'])
        # assert len(response['detail']['friends']) == 1
        # assert response['detail']['friends'] == [second_telegram_user.telegram_id]

        data_for_create_referral = {
            'telegram_user_id': first_telegram_user.telegram_id,
            'friend_telegram_id': third_telegram_user.telegram_id,
        }

        response = self._client.post(url=self._url, headers=self._headers, json=data_for_create_referral)
        assert response.status_code == status.HTTP_201_CREATED
        response = response.json()
        assert response['detail']['telegram_id'] == first_telegram_user.telegram_id
        assert len(response['detail']['friends']) == 2
        print(response['detail']['telegram_id'])
        print(response['detail']['friends'])
        assert response['detail']['friends'] == [second_telegram_user.telegram_id, third_telegram_user.telegram_id]
