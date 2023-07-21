from typing import List

from sqlalchemy import func

from db.core import Session
from db.models import Users, UsersText
from main.functions import get_today_timestamp


def get_users_who_not_read_today() -> List[Users]:
    """Get users who not read today"""
    with Session() as session:
        return session.query(Users).filter(
                Users.telegram_id.notin_(
                    session.query(UsersText.user_telegram_id)
                    .group_by(UsersText.user_telegram_id)
                    .having(func.max(UsersText.date) == int(get_today_timestamp()))
                )
            ).all()
