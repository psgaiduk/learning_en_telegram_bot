from db.core import Session
from db.models import Texts


def create_text(text: str):
    """Function for create new text in database."""
    with Session() as session:
        new_text = Texts(level=1, text=text)
        session.add(new_text)
        session.commit()
        session.refresh(new_text)
