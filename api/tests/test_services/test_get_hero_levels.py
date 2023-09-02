from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import HeroLevels
from settings import settings
from tests.fixtures import create_test_database, hero_level_mock
from tests.connect_db import db_session


@mark.usefixtures('create_test_database', 'hero_level_mock')
class TestGetHeroLevelsAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)
        cls._url = '/api/v1/service/hero_levels/'

    def test_get_hero_levels(self):
        response = self._client.get(url=self._url, headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()

        with db_session() as db:
            db_hero_levels = db.query(HeroLevels).all()
            assert len(response) == len(db_hero_levels)
            for hero_level, resp_hero_level in zip(db_hero_levels, response):
                assert hero_level.id == resp_hero_level['id']
                assert hero_level.title == resp_hero_level['title']
                assert hero_level.need_experience == resp_hero_level['need_experience']

    def test_not_get_hero_levels_without_api_key(self):
        response = self._client.get(url=self._url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
