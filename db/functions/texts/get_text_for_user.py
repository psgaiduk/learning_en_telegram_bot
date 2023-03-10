from random import choice

from db.core import Session
from db.models import users_texts, Texts
from db.utils import add_new_text_to_db


def get_text_for_user(telegram_id: int):
    """"""
    with Session() as session:
        subquery = session.query(
            users_texts
        ).filter_by(user_telegram_id=telegram_id).subquery()

        texts = session.query(
            Texts, subquery
        ).join(
            subquery, isouter=True
        ).filter_by(
            user_telegram_id=None
        ).filter(
            Texts.level == 1
        ).all()

        if not texts:
            return add_new_text_to_db()

        random_text = choice(texts)[0]

        return random_text.text, random_text.id
