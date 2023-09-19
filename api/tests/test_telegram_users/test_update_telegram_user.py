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

    def test_update_fields(self):

        with db_session() as db:
            old_telegram_user = db.query(Users).first()
            telegram_id = old_telegram_user.telegram_id
            
            new_experience = old_telegram_user.experience + 100
            assert old_telegram_user.experience != new_experience

            levels_ids = [1, 2, 3]
            levels_ids.remove(old_telegram_user.level_en_id)
            new_level_id = choice(levels_ids)
            assert old_telegram_user.level_en_id != new_level_id

            new_user_name = old_telegram_user.user_name + ' test'
            assert old_telegram_user.user_name != new_user_name

            hero_levels_ids = [1, 2, 3, 4, 5]
            hero_levels_ids.remove(old_telegram_user.hero_level_id)
            new_hero_level_id = choice(hero_levels_ids)
            assert old_telegram_user.hero_level_id != new_hero_level_id

            new_previous_stage = old_telegram_user.previous_stage + ' test'
            assert old_telegram_user.previous_stage != new_previous_stage

            new_stage = old_telegram_user.stage + ' test'
            assert old_telegram_user.stage != new_stage

            params_for_update_user = {
                'telegram_id': telegram_id,
                'level_en_id': new_level_id,
                'main_language_id': old_telegram_user.main_language_id,
                'user_name': new_user_name,
                'experience': new_experience,
                'hero_level_id': new_hero_level_id,
                'previous_stage': new_previous_stage,
                'stage': new_stage,
            }

            response = self._client.patch(
                url=f'/api/v1/telegram_user/{telegram_id}',
                headers=self._headers,
                json=params_for_update_user,
            )
            assert response.status_code == status.HTTP_200_OK
            assert response.json()['detail']
            response = response.json()['detail']
            new_telegram_user = db.query(Users).filter(Users.telegram_id == telegram_id).first()
            db.refresh(new_telegram_user)
            assert new_telegram_user.experience == new_experience
            assert response['experience'] == new_experience
            assert new_telegram_user.level_en_id == new_level_id
            assert response['level_en_id'] == new_level_id
            assert response['level_en']['id'] == new_level_id
            assert new_telegram_user.user_name == new_user_name
            assert response['user_name'] == new_user_name
            assert new_telegram_user.hero_level_id == new_hero_level_id
            assert response['hero_level_id'] == new_hero_level_id
            assert response['hero_level']['id'] == new_hero_level_id
            assert new_telegram_user.previous_stage == new_previous_stage
            assert response['previous_stage'] == new_previous_stage
            assert new_telegram_user.stage == new_stage
            assert response['stage'] == new_stage

    def test_update_telegram_user_without_stage(self):
        with db_session() as db:
            old_telegram_user = db.query(Users).first()
            telegram_id = old_telegram_user.telegram_id

            params_for_update_user = {
                'telegram_id': telegram_id,
                'level_en_id': 1,
                'main_language_id': old_telegram_user.main_language_id,
                'user_name': 'test',
                'experience': 0,
                'hero_level_id': 1,
                'previous_stage': '',
            }

            response = self._client.patch(
                url=f'/api/v1/telegram_user/{telegram_id}',
                headers=self._headers,
                json=params_for_update_user,
            )
            assert response.status_code == status.HTTP_200_OK
            response = response.json()['detail']
            assert response['stage'] == old_telegram_user.stage

    def test_update_telegram_user_without_previous_stage(self):
        with db_session() as db:
            old_telegram_user = db.query(Users).first()
            telegram_id = old_telegram_user.telegram_id

            params_for_update_user = {
                'telegram_id': telegram_id,
                'level_en_id': 1,
                'main_language_id': old_telegram_user.main_language_id,
                'user_name': 'test',
                'experience': 0,
                'hero_level_id': 1,
            }

            response = self._client.patch(
                url=f'/api/v1/telegram_user/{telegram_id}',
                headers=self._headers,
                json=params_for_update_user,
            )
            assert response.status_code == status.HTTP_200_OK
            response = response.json()['detail']
            assert response['previous_stage'] == old_telegram_user.previous_stage

    def test_update_telegram_user_without_name(self):
        with db_session() as db:
            old_telegram_user = db.query(Users).first()
            telegram_id = old_telegram_user.telegram_id

            params_for_update_user = {
                'telegram_id': telegram_id,
                'level_en_id': 1,
                'main_language_id': old_telegram_user.main_language_id,
                'experience': 0,
                'hero_level_id': 1,
            }

            response = self._client.patch(
                url=f'/api/v1/telegram_user/{telegram_id}',
                headers=self._headers,
                json=params_for_update_user,
            )
            assert response.status_code == status.HTTP_200_OK
            response = response.json()['detail']
            assert response['user_name'] == old_telegram_user.user_name

    def test_update_telegram_user_without_level_id(self):
        with db_session() as db:
            old_telegram_user = db.query(Users).first()
            telegram_id = old_telegram_user.telegram_id

            params_for_update_user = {
                'telegram_id': telegram_id,
                'main_language_id': old_telegram_user.main_language_id,
                'experience': 0,
                'hero_level_id': 1,
            }

            response = self._client.patch(
                url=f'/api/v1/telegram_user/{telegram_id}',
                headers=self._headers,
                json=params_for_update_user,
            )
            assert response.status_code == status.HTTP_200_OK
            response = response.json()['detail']
            assert response['level_en_id'] == old_telegram_user.level_en_id

    def test_update_telegram_user_without_experience(self):
        with db_session() as db:
            old_telegram_user = db.query(Users).first()
            telegram_id = old_telegram_user.telegram_id

            params_for_update_user = {
                'telegram_id': telegram_id,
                'main_language_id': old_telegram_user.main_language_id,
                'hero_level_id': 1,
            }

            response = self._client.patch(
                url=f'/api/v1/telegram_user/{telegram_id}',
                headers=self._headers,
                json=params_for_update_user,
            )
            assert response.status_code == status.HTTP_200_OK
            response = response.json()['detail']
            assert response['experience'] == old_telegram_user.experience

    def test_update_telegram_user_without_hero_level_id(self):
        with db_session() as db:
            old_telegram_user = db.query(Users).first()
            telegram_id = old_telegram_user.telegram_id

            params_for_update_user = {
                'telegram_id': telegram_id,
                'main_language_id': old_telegram_user.main_language_id,
            }

            response = self._client.patch(
                url=f'/api/v1/telegram_user/{telegram_id}',
                headers=self._headers,
                json=params_for_update_user,
            )
            assert response.status_code == status.HTTP_200_OK
            response = response.json()['detail']
            assert response['hero_level_id'] == old_telegram_user.hero_level_id

    def test_update_telegram_user_without_main_language_id(self):
        with db_session() as db:
            old_telegram_user = db.query(Users).first()
            telegram_id = old_telegram_user.telegram_id

            params_for_update_user = {
                'telegram_id': telegram_id,
            }

            response = self._client.patch(
                url=f'/api/v1/telegram_user/{telegram_id}',
                headers=self._headers,
                json=params_for_update_user,
            )
            assert response.status_code == status.HTTP_200_OK
            response = response.json()['detail']
            assert response['main_language_id'] == old_telegram_user.main_language_id

    def test_update_telegram_user_without_telegram_id(self):
        with db_session() as db:
            old_telegram_user = db.query(Users).first()
            telegram_id = old_telegram_user.telegram_id

            params_for_update_user = {
                'hero_level_id': 2,
            }

            response = self._client.patch(
                url=f'/api/v1/telegram_user/{telegram_id}',
                headers=self._headers,
                json=params_for_update_user,
            )
            assert response.status_code == status.HTTP_200_OK
            response = response.json()['detail']
            assert response['hero_level_id'] == 2

    def test_not_update_telegram_user_without_data(self):
        with db_session() as db:
            old_telegram_user = db.query(Users).first()
            telegram_id = old_telegram_user.telegram_id

            params_for_update_user = {}

            response = self._client.patch(
                url=f'/api/v1/telegram_user/{telegram_id}',
                headers=self._headers,
                json=params_for_update_user,
            )
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_update_telegram_user_without_api_key(self):
        with db_session() as db:
            old_telegram_user = db.query(Users).first()
            telegram_id = old_telegram_user.telegram_id

            params_for_update_user = {}

            response = self._client.patch(
                url=f'/api/v1/telegram_user/{telegram_id}',
                json=params_for_update_user,
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

