from pytest import fixture

from database import get_db
from models import LevelsEn


@fixture
def level_en_mock():
    with get_db() as db:
        level_1 = LevelsEn(
            id=1,
            title='A1',
            description='Beginner',
            order=1,
        )
        level_2 = LevelsEn(
            id=2,
            title='A2',
            description='Elementary',
            order=2,
        )
        level_3 = LevelsEn(
            id=3,
            title='B1',
            description='Intermediate',
            order=3,
        )
        level_4 = LevelsEn(
            id=4,
            title='B2',
            description='Upper Intermediate',
            order=4,
        )
        level_5 = LevelsEn(
            id=5,
            title='C1',
            description='Advanced',
            order=5,
        )
        level_6 = LevelsEn(
            id=6,
            title='C2',
            description='Proficiency',
            order=6,
        )

        db.add(level_1)
        db.add(level_2)
        db.add(level_3)
        db.add(level_4)
        db.add(level_5)
        db.add(level_6)
        db.commit()
