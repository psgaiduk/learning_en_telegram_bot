from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import LevelsEn
from settings import settings
from tests.fixtures import create_test_database, level_en_mock
from tests.connect_db import db_session


@mark.usefixtures('create_test_database', 'level_en_mock')
class TestGetEnglishLevelsAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)

    def test_get_english_levels(self):
        response = self._client.get('/api/v1/service/english_levels/', headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()

        with db_session() as db:
            db_levels = db.query(LevelsEn).all()
            assert len(db_levels) == len(response)
            for level, resp_level in zip(db_levels, response):
                assert level.id == resp_level['id']
                assert level.title == resp_level['title']
                assert level.description == resp_level['description']

    def test_not_get_english_levels_without_api_key(self):
        response = self._client.get('/api/v1/service/english_levels/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
