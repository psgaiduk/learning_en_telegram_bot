from db.core import Session
from db.models import CurrentUserText


async def update_current_text_user(telegram_id: int, next_sentences: list, previous_sentences: list):
    """Update item current text user for user."""
    with Session() as session:
        current_text = session.query(
            CurrentUserText
        ).filter(
            CurrentUserText.telegram_id == telegram_id,
        ).first()
        current_text.next_sentences = next_sentences
        current_text.previous_sentences = previous_sentences
        session.commit()

