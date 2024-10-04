from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import HeroLevels
from settings import settings
from tests.fixtures import create_test_database, hero_level_mock
from tests.connect_db import db_session


@mark.usefixtures("create_test_database", "hero_level_mock")
class TestGetHeroLevelByNumberAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {"X-API-Key": settings.api_key}
        cls._client = TestClient(app)
        cls._url = "/api/v1/service/hero_levels"

    def test_good_get_hero_level_by_number(self, hero_level_mock):
        with db_session() as db:
            db_hero_level = db.query(HeroLevels).first()
            hero_number = db_hero_level.id

        response = self._client.get(url=f"{self._url}/{hero_number}/", headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()

        assert db_hero_level.id == response["id"]
        assert db_hero_level.title == response["title"]
        assert db_hero_level.need_experience == response["need_experience"]
        assert db_hero_level.count_sentences == response["count_sentences"]
        assert db_hero_level.count_games == response["count_games"]
        assert db_hero_level.order == response["order"]

    def test_not_get_hero_level_by_number(self):
        with db_session() as db:
            db_hero_level = db.query(HeroLevels).order_by(HeroLevels.id.desc()).first()
            hero_number = db_hero_level.id + 1

        response = self._client.get(url=f"{self._url}/{hero_number}/", headers=self._headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_not_get_hero_level_by_number_without_api_key(self):
        with db_session() as db:
            db_hero_level = db.query(HeroLevels).first()
            hero_number = db_hero_level.id

        response = self._client.get(url=f"{self._url}/{hero_number}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
