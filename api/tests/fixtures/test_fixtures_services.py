from pytest import fixture

from database import get_db
from models import LevelsEn, TypeWords


@fixture
def level_en_mock():

    levels_data = [
        {'id': 1, 'title': 'A1', 'description': 'Beginner', 'order': 1},
        {'id': 2, 'title': 'A2', 'description': 'Elementary', 'order': 2},
        {'id': 3, 'title': 'B1', 'description': 'Intermediate', 'order': 3},
        {'id': 4, 'title': 'B2', 'description': 'Upper Intermediate', 'order': 4},
        {'id': 5, 'title': 'C1', 'description': 'Advanced', 'order': 5},
    ]

    with get_db() as db:
        for level_data in levels_data:
            level = LevelsEn(**level_data)
            db.add(level)
        db.commit()

#
# @fixture
# def type_words_mock():
#
#     levels_data = [
#         {'type_word_id': 1, 'title': 'word'},
#         {'type_word_id': 2, 'title': 'phrase verb'},
#         {'type_word_id': 3, 'title': 'idiom'},
#     ]
#
#     with get_db() as db:
#         for level_data in TypeWords:
#             level = LevelsEn(**level_data)
#             db.add(level)
#         db.commit()
