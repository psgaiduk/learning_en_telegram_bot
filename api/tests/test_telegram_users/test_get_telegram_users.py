from random import choice

from fastapi.testclient import TestClient
from main import app
from fastapi import status
from pytest import mark

from tests.connect_db import db_session
from tests.fixtures import (
    create_test_database,
    level_en_mock,
    hero_level_mock,
    main_language_mock,
    telegram_users_mock,
)
from models import Users
from settings import settings


@mark.usefixtures(
    'create_test_database', 'level_en_mock', 'main_language_mock', 'hero_level_mock', 'telegram_users_mock',
)
class TestUpdateTelegramUserAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)

    def test_get_telegram_user(self):
        with db_session() as db:
            telegram_user = db.query(Users).first()
            telegram_id = telegram_user.telegram_id

            response = self._client.get(
                url=f'/api/v1/telegram_user/{telegram_id}',
                headers=self._headers,
            )
            assert response.status_code == status.HTTP_200_OK
            response = response.json()
            assert response['detail']['experience'] == telegram_user.experience
            assert response['detail']['level_en_id'] == telegram_user.level_en_id
            assert response['detail']['level_en']['id'] == telegram_user.level_en_id
            assert response['detail']['user_name'] == telegram_user.user_name
            assert response['detail']['hero_level_id'] == telegram_user.hero_level_id
            assert response['detail']['hero_level']['id'] == telegram_user.hero_level_id
            assert response['detail']['previous_stage'] == telegram_user.previous_stage
            assert response['detail']['stage'] == telegram_user.stage

    def test_not_get_telegram_user_without_api_key(self):
        with db_session() as db:
            old_telegram_user = db.query(Users).first()
            telegram_id = old_telegram_user.telegram_id

            response = self._client.get(
                url=f'/api/v1/telegram_user/{telegram_id}',
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_get_telegram_user(self):
        with db_session() as db:
            telegram_user = db.query(Users).order_by(Users.telegram_id).first()
            telegram_id = telegram_user.telegram_id + 1

            response = self._client.get(
                url=f'/api/v1/telegram_user/{telegram_id}',
                headers=self._headers,
            )
            assert response.status_code == status.HTTP_404_NOT_FOUND
