from random import choice

from db.core import Session
from db.models import users_texts, Texts, Users


async def get_text_for_user(user: Users) -> tuple:
    """"""
    with Session() as session:
        subquery = session.query(
            users_texts
        ).filter(
            users_texts.c.user_telegram_id == user.telegram_id,
            users_texts.c.language == f'{user.main_language}{user.learn_language}'
        ).subquery()

        texts = session.query(
            Texts, subquery
        ).join(
            subquery, isouter=True,
        ).filter_by(
            user_telegram_id=None,
        ).filter(
            Texts.level == 3,
        )
        texts = texts.all()

        main_text = None
        translate_text = None

        if not texts:
            return main_text, translate_text

        random_text = choice(texts)[0]

        if user.main_language == 'ru':
            translate_text = random_text.text_ru
        elif user.main_language == 'fr':
            translate_text = random_text.text_fr
        elif user.main_language == 'es':
            translate_text = random_text.text_es
        elif user.main_language == 'ge':
            translate_text = random_text.text_ge
        else:
            translate_text = random_text.text_en

        if user.learn_language == 'en':
            main_text = random_text.text_en
        elif user.learn_language == 'fr':
            main_text = random_text.text_fr
        elif user.learn_language == 'es':
            main_text = random_text.text_es
        elif user.learn_language == 'ge':
            main_text = random_text.text_ge
        else:
            main_text = random_text.text_ru

        return main_text, translate_text, random_text.id
