from pytest import fixture

from tests.connect_db import db_session
from models import HeroLevels, LevelsEn, TypeWords, MainLanguages


@fixture()
def level_en_mock():

    levels_data = [
        {"id": 1, "title": "A1", "description": "Beginner", "order": 1},
        {"id": 2, "title": "A2", "description": "Elementary", "order": 2},
        {"id": 3, "title": "B1", "description": "Intermediate", "order": 3},
        {"id": 4, "title": "B2", "description": "Upper Intermediate", "order": 4},
        {"id": 5, "title": "C1", "description": "Advanced", "order": 5},
    ]

    with db_session() as db:
        for level_data in levels_data:
            level = LevelsEn(**level_data)
            db.add(level)
        db.commit()


@fixture
def type_words_mock():

    levels_data = [
        {"type_word_id": 1, "title": "word"},
        {"type_word_id": 2, "title": "phrase verb"},
        {"type_word_id": 3, "title": "idiom"},
    ]

    with db_session() as db:
        for level_data in levels_data:
            level = TypeWords(**level_data)
            db.add(level)
        db.commit()


@fixture
def main_language_mock():

    languages_data = [
        {"id": 1, "title": "ru", "description": "Русский язык"},
    ]

    with db_session() as db:
        for language_data in languages_data:
            language = MainLanguages(**language_data)
            db.add(language)
        db.commit()


@fixture
def hero_level_mock():

    hero_levels_data = [
        {
            "id": 1,
            "title": "1",
            "need_experience": 0,
            "count_sentences": 5,
            "count_games": 0,
            "order": 1,
        },
        {
            "id": 2,
            "title": "2",
            "need_experience": 100,
            "count_sentences": 6,
            "count_games": 0,
            "order": 2,
        },
        {
            "id": 3,
            "title": "3",
            "need_experience": 200,
            "count_sentences": 7,
            "count_games": 0,
            "order": 3,
        },
        {
            "id": 4,
            "title": "4",
            "need_experience": 300,
            "count_sentences": 8,
            "count_games": 0,
            "order": 4,
        },
        {
            "id": 5,
            "title": "5",
            "need_experience": 400,
            "count_sentences": 9,
            "count_games": 1,
            "order": 5,
        },
    ]

    with db_session() as db:
        for hero_level_data in hero_levels_data:
            hero_level = HeroLevels(**hero_level_data)
            db.add(hero_level)
        db.commit()
