from typing import List

from db.core import Session
from db.models import TextReminder


def get_text_reminders() -> List[TextReminder]:
    """Get all text reminders"""
    with Session() as session:
        return session.query(TextReminder).all()
