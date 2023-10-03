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
)
from models import Users
from settings import settings


@mark.usefixtures('create_test_database', 'level_en_mock', 'main_language_mock', 'hero_level_mock')
class TestTelegramUserAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)

    def test_create_telegram_user(self):

        params_for_create_user = {
            'telegram_id': 123456789,
            'level_en_id': 1,
            'main_language_id': 1,
            'user_name': 'Test User',
            'experience': 0,
            'hero_level_id': 1,
            'previous_stage': '',
            'stage': '',
        }

        response = self._client.post(f'/api/v1/telegram_user/', headers=self._headers, json=params_for_create_user)
        assert response.status_code == status.HTTP_201_CREATED
        
        with db_session() as db:
            telegram_user = db.query(Users).filter(Users.telegram_id == params_for_create_user['telegram_id']).first()
            assert telegram_user.telegram_id == params_for_create_user['telegram_id']
            assert telegram_user.level_en_id == params_for_create_user['level_en_id']
            assert telegram_user.main_language_id == params_for_create_user['main_language_id']
            assert telegram_user.user_name == params_for_create_user['user_name']
            assert telegram_user.experience == params_for_create_user['experience']
            assert telegram_user.hero_level_id == params_for_create_user['hero_level_id']
            assert telegram_user.previous_stage == params_for_create_user['previous_stage']
            assert telegram_user.stage == params_for_create_user['stage']

    def test_not_create_telegram_user_without_api_key(self):
        params_for_create_user = {
            'telegram_id': 123456789,
            'level_en_id': 1,
            'main_language_id': 1,
            'user_name': 'Test User',
            'experience': 0,
            'hero_level_id': 1,
            'previous_stage': '',
            'stage': '',
        }

        response = self._client.post(f'/api/v1/telegram_user/', json=params_for_create_user)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_create_telegram_user_without_telegram_id(self):
        params_for_create_user = {
            'level_en_id': 1,
            'main_language_id': 1,
            'user_name': 'Test User',
            'experience': 0,
            'hero_level_id': 1,
            'previous_stage': '',
            'stage': '',
        }

        response = self._client.post(f'/api/v1/telegram_user/', headers=self._headers, json=params_for_create_user)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_not_create_telegram_user_without_main_language_id(self):
        params_for_create_user = {
            'telegram_id': 123456789,
            'level_en_id': 1,
            'user_name': 'Test User',
            'experience': 0,
            'hero_level_id': 1,
            'previous_stage': '',
            'stage': '',
        }

        response = self._client.post(f'/api/v1/telegram_user/', headers=self._headers, json=params_for_create_user)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_telegram_user_without_user_name(self):
        params_for_create_user = {
            'telegram_id': 123456789,
            'level_en_id': 1,
            'main_language_id': 1,
            'experience': 0,
            'hero_level_id': 1,
            'previous_stage': '',
            'stage': '',
        }

        response = self._client.post(f'/api/v1/telegram_user/', headers=self._headers, json=params_for_create_user)
        assert response.status_code == status.HTTP_201_CREATED

        with db_session() as db:
            telegram_user = db.query(Users).filter(Users.telegram_id == params_for_create_user['telegram_id']).first()
            assert telegram_user.user_name == 'New client'

    def test_create_telegram_user_without_level_en_id(self):
        params_for_create_user = {
            'telegram_id': 123456789,
            'main_language_id': 1,
            'experience': 0,
            'hero_level_id': 1,
            'previous_stage': '',
            'stage': '',
        }

        response = self._client.post(f'/api/v1/telegram_user/', headers=self._headers, json=params_for_create_user)
        assert response.status_code == status.HTTP_201_CREATED

        with db_session() as db:
            telegram_user = db.query(Users).filter(Users.telegram_id == params_for_create_user['telegram_id']).first()
            assert telegram_user.level_en_id is None

    def test_create_telegram_user_without_experience(self):
        params_for_create_user = {
            'telegram_id': 123456789,
            'level_en_id': 1,
            'main_language_id': 1,
            'user_name': 'Test User',
            'hero_level_id': 1,
            'previous_stage': '',
            'stage': '',
        }

        response = self._client.post(f'/api/v1/telegram_user/', headers=self._headers, json=params_for_create_user)
        assert response.status_code == status.HTTP_201_CREATED

        with db_session() as db:
            telegram_user = db.query(Users).filter(Users.telegram_id == params_for_create_user['telegram_id']).first()
            assert telegram_user.experience == 0

    def test_not_create_telegram_user_without_hero_level_id(self):
        params_for_create_user = {
            'telegram_id': 123456789,
            'level_en_id': 1,
            'main_language_id': 1,
            'user_name': 'Test User',
            'experience': 0,
            'previous_stage': '',
            'stage': '',
        }

        response = self._client.post(f'/api/v1/telegram_user/', headers=self._headers, json=params_for_create_user)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_telegram_user_without_previous_stage(self):
        params_for_create_user = {
            'telegram_id': 123456789,
            'level_en_id': 1,
            'main_language_id': 1,
            'user_name': 'Test User',
            'experience': 0,
            'hero_level_id': 1,
            'stage': '',
        }

        response = self._client.post(f'/api/v1/telegram_user/', headers=self._headers, json=params_for_create_user)
        assert response.status_code == status.HTTP_201_CREATED

        with db_session() as db:
            telegram_user = db.query(Users).filter(Users.telegram_id == params_for_create_user['telegram_id']).first()
            assert telegram_user.previous_stage is None

    def test_create_telegram_user_without_stage(self):
        params_for_create_user = {
            'telegram_id': 123456789,
            'level_en_id': 1,
            'main_language_id': 1,
            'user_name': 'Test User',
            'experience': 0,
            'hero_level_id': 1,
            'previous_stage': '',
        }

        response = self._client.post(f'/api/v1/telegram_user/', headers=self._headers, json=params_for_create_user)
        assert response.status_code == status.HTTP_201_CREATED

        with db_session() as db:
            telegram_user = db.query(Users).filter(Users.telegram_id == params_for_create_user['telegram_id']).first()
            assert telegram_user.stage is None
