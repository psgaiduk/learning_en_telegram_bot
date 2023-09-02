from fastapi.testclient import TestClient
from fastapi import status
from pytest import mark

from main import app
from models import MainLanguages
from settings import settings
from tests.fixtures import create_test_database, main_language_mock
from tests.connect_db import db_session


@mark.usefixtures('create_test_database', 'main_language_mock')
class TestGetLanguagesAPI:

    @classmethod
    def setup_class(cls):
        cls._headers = {'X-API-Key': settings.api_key}
        cls._client = TestClient(app)

    def test_get_languages(self):
        response = self._client.get('/api/v1/service/languages/', headers=self._headers)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()

        with db_session() as db:
            db_languages = db.query(MainLanguages).all()
            assert len(response) == len(db_languages)
            for language, resp_language in zip(db_languages, response):
                assert language.id == resp_language['id']
                assert language.title == resp_language['title']
                assert language.description == resp_language['description']

    def test_not_get_languages_without_api_key(self):
        response = self._client.get('/api/v1/service/languages/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
