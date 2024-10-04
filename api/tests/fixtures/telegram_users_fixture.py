from faker import Faker
from pytest import fixture

from tests.connect_db import db_session
from models import LevelsEn, MainLanguages, Users
from tests.fixtures.test_fixtures_services import (
    hero_level_mock,
    level_en_mock,
    main_language_mock,
)


fake = Faker()
fake_ru = Faker("ru_RU")


@fixture
def telegram_users_mock(level_en_mock, main_language_mock, hero_level_mock):
    with db_session() as db:
        levels = db.query(LevelsEn).all()
        main_languages = db.query(MainLanguages).all()

        for level_en in levels:
            for language in main_languages:

                telegram_user = {
                    "telegram_id": fake.random_int(min=1, max=100000000),
                    "level_en_id": level_en.id,
                    "main_language_id": language.id,
                    "user_name": fake.name(),
                    "experience": fake.random_int(min=1, max=100000000),
                    "hero_level_id": 1,
                    "previous_stage": fake_ru.word(),
                    "stage": fake_ru.word(),
                }

                db.add(Users(**telegram_user))

        db.commit()
