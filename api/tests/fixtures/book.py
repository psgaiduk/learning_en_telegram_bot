from pytest import fixture

from database import get_db
from models import Words


@fixture
def word_mock():

    with get_db() as db:
        word1 = Words(
            type_word_id=1,
            word="Hello",
            translation={"ru": "Привет"}
        )

        word2 = Words(
            type_word_id=2,
            word="World",
            translation={"ru": "Мир"}
        )

        word3 = Words(
            type_word_id=3,
            word="Python",
            translation={"ru": "Питон"}
        )

        db.add(word1)
        db.add(word2)
        db.add(word3)

        db.commit()
