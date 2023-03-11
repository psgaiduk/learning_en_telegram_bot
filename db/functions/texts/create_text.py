from db.core import Session
from db.models import Texts


def create_text(text_en: str, text_ru: str, text_ge: str, text_es: str, text_fr: str):
    """Function for create new text in database."""
    with Session() as session:
        new_text = Texts(level=3, text_en=text_en, text_ru=text_ru, text_ge=text_ge, text_es=text_es, text_fr=text_fr)
        session.add(new_text)
        session.commit()
        session.refresh(new_text)
