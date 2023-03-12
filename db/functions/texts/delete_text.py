from db.core import Session
from db.models import Texts


def delete_text(text_id: int):
    """Function for create new text in database."""
    with Session() as session:
        session.query(
            Texts
        ).filter(
            Texts.id == text_id,
        ).delete()
        session.commit()
