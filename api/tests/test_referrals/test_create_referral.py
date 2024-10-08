from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import Users, UsersReferrals
from settings import settings
from tests.connect_db import db_session

from tests.fixtures import *


@mark.usefixtures("create_test_database", "telegram_users_mock")
class TestCreateReferralAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {"X-API-Key": settings.api_key}
        cls._client = TestClient(app)
        cls._url = "/api/v1/referrals/"

    def test_create_referral_user(self):
        with db_session() as db:
            telegram_users = db.query(Users).all()
            first_telegram_user = telegram_users[0]
            second_telegram_user = telegram_users[1]
            third_telegram_user = telegram_users[2]

        data_for_create_referral = {
            "telegram_user_id": first_telegram_user.telegram_id,
            "friend_telegram_id": second_telegram_user.telegram_id,
        }

        response = self._client.post(url=self._url, headers=self._headers, json=data_for_create_referral)
        assert response.status_code == status.HTTP_201_CREATED
        response = response.json()
        assert response["detail"]["telegram_id"] == first_telegram_user.telegram_id
        assert len(response["detail"]["friends"]) == 1
        assert response["detail"]["friends"] == [second_telegram_user.telegram_id]

        data_for_create_referral = {
            "telegram_user_id": first_telegram_user.telegram_id,
            "friend_telegram_id": third_telegram_user.telegram_id,
        }

        response = self._client.post(url=self._url, headers=self._headers, json=data_for_create_referral)
        assert response.status_code == status.HTTP_201_CREATED
        response = response.json()
        assert response["detail"]["telegram_id"] == first_telegram_user.telegram_id
        assert len(response["detail"]["friends"]) == 2
        assert response["detail"]["friends"] == [
            second_telegram_user.telegram_id,
            third_telegram_user.telegram_id,
        ]

        with db_session() as db:
            assert db.query(UsersReferrals).count() == 2
            assert (
                db.query(UsersReferrals)
                .filter(UsersReferrals.friend_telegram_id == second_telegram_user.telegram_id)
                .first()
            )
            assert (
                db.query(UsersReferrals)
                .filter(UsersReferrals.friend_telegram_id == third_telegram_user.telegram_id)
                .first()
            )
            assert (
                db.query(UsersReferrals).filter(UsersReferrals.telegram_id == first_telegram_user.telegram_id).count()
                == 2
            )

    def test_not_create_again_referral_user(self):
        with db_session() as db:
            telegram_users = db.query(Users).all()
            first_telegram_user = telegram_users[0]
            second_telegram_user = telegram_users[1]
            third_telegram_user = telegram_users[2]

        data_for_create_referral = {
            "telegram_user_id": first_telegram_user.telegram_id,
            "friend_telegram_id": second_telegram_user.telegram_id,
        }

        response = self._client.post(url=self._url, headers=self._headers, json=data_for_create_referral)
        assert response.status_code == status.HTTP_201_CREATED
        response = response.json()
        assert response["detail"]["telegram_id"] == first_telegram_user.telegram_id
        assert len(response["detail"]["friends"]) == 1
        assert response["detail"]["friends"] == [second_telegram_user.telegram_id]

        data_for_create_referral = {
            "telegram_user_id": first_telegram_user.telegram_id,
            "friend_telegram_id": second_telegram_user.telegram_id,
        }

        response = self._client.post(url=self._url, headers=self._headers, json=data_for_create_referral)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        data_for_create_referral = {
            "telegram_user_id": third_telegram_user.telegram_id,
            "friend_telegram_id": second_telegram_user.telegram_id,
        }

        response = self._client.post(url=self._url, headers=self._headers, json=data_for_create_referral)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_create_referral_user_if_wrong_telegram_id(self):
        with db_session() as db:
            telegram_users = db.query(Users).order_by(Users.telegram_id.desc()).first()
            first_telegram_user = telegram_users
            wrong_telegram_id = first_telegram_user.telegram_id + 1

        data_for_create_referral = {
            "telegram_user_id": first_telegram_user.telegram_id,
            "friend_telegram_id": wrong_telegram_id,
        }

        response = self._client.post(url=self._url, headers=self._headers, json=data_for_create_referral)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        data_for_create_referral = {
            "telegram_user_id": wrong_telegram_id,
            "friend_telegram_id": first_telegram_user.telegram_id,
        }

        response = self._client.post(url=self._url, headers=self._headers, json=data_for_create_referral)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_no_create_without_api_key(self):
        with db_session() as db:
            telegram_users = db.query(Users).all()
            first_telegram_user = telegram_users[0]
            second_telegram_user = telegram_users[1]

        data_for_create_referral = {
            "telegram_user_id": first_telegram_user.telegram_id,
            "friend_telegram_id": second_telegram_user.telegram_id,
        }

        response = self._client.post(url=self._url, json=data_for_create_referral)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_no_create_with_wrong_api_key(self):
        with db_session() as db:
            telegram_users = db.query(Users).all()
            first_telegram_user = telegram_users[0]
            second_telegram_user = telegram_users[1]

        data_for_create_referral = {
            "telegram_user_id": first_telegram_user.telegram_id,
            "friend_telegram_id": second_telegram_user.telegram_id,
        }

        response = self._client.post(url=self._url, json=data_for_create_referral, headers={"X-API-Key": "test"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
