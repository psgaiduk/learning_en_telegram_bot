from datetime import datetime

from db.core import Session
from db.models import UsersText


async def get_today_text_by_telegram_id(telegram_id: int) -> UsersText:
    """"""
    with Session() as session:
        text_today = session.query(UsersText).filter(
            UsersText.user_telegram_id == telegram_id,
            UsersText.date == int(datetime.utcnow().replace(hour=0, minute=0, second=0).timestamp()),
        )
        return text_today.first()
