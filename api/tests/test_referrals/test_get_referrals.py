from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import Users, UsersReferrals
from settings import settings
from tests.connect_db import db_session

from tests.fixtures import *


@mark.usefixtures('create_test_database', 'referrals_fixture')
class TestGetReferralAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)
        cls._url = '/api/v1/referrals/'

    def test_get_referral_for_users(self):
        with db_session() as db:
            telegram_users_ids = [item[0] for item in db.query(UsersReferrals.telegram_id).distinct().all()]
            telegram_users = db.query(Users).filter(Users.telegram_id.in_(telegram_users_ids)).all()

            for telegram_user in telegram_users:
                response = self._client.get(url=f'{self._url}{telegram_user.telegram_id}/', headers=self._headers)
                assert response.status_code == status.HTTP_200_OK
                response = response.json()
                friends = [referral.friend.telegram_id for referral in telegram_user.referrals]
                assert response['detail']['telegram_id'] == telegram_user.telegram_id
                assert len(response['detail']['friends']) == len(friends)
                assert response['detail']['friends'] == friends

    def test_not_get_referral_for_user_not_found(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id.desc()).first()
            telegram_user_id = telegram_user.telegram_id + 1

        response = self._client.get(url=f'{self._url}{telegram_user_id}/', headers=self._headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_referral_for_user_without_referrals(self):
        with db_session() as db:
            telegram_users_ids = [item[0] for item in db.query(UsersReferrals.telegram_id).distinct().all()]
            telegram_user = db.query(Users).filter(Users.telegram_id.not_in(telegram_users_ids)).first()

        response = self._client.get(url=f'{self._url}{telegram_user.telegram_id}/', headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        assert response['detail']['telegram_id'] == telegram_user.telegram_id
        assert response['detail']['friends'] == []

    def test_not_get_referral_for_user_without_api_key(self):
        with db_session() as db:
            telegram_users_ids = [item[0] for item in db.query(UsersReferrals.telegram_id).distinct().all()]
            telegram_user = db.query(Users).filter(Users.telegram_id.not_in(telegram_users_ids)).first()

        response = self._client.get(url=f'{self._url}{telegram_user.telegram_id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_get_referral_for_user_with_wrong_api_key(self):
        with db_session() as db:
            telegram_users_ids = [item[0] for item in db.query(UsersReferrals.telegram_id).distinct().all()]
            telegram_user = db.query(Users).filter(Users.telegram_id.not_in(telegram_users_ids)).first()

        response = self._client.get(url=f'{self._url}{telegram_user.telegram_id}/', headers={'X-API-Key': 'test'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
