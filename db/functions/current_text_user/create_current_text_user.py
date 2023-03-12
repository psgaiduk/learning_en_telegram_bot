from db.core import Session
from db.models import CurrentUserText


async def create_current_text_user(telegram_id: int, text_id: int, next_sentences: list, previous_sentences: list):
    """Create item current text user for user."""
    with Session() as session:
        new_item = CurrentUserText(
            telegram_id=telegram_id,
            text_id=text_id,
            next_sentences=next_sentences,
            previous_sentences=previous_sentences,
        )
        session.add(new_item)
        session.commit()
        session.refresh(new_item)

    return new_item
