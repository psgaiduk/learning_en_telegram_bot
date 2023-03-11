from db.core import Session
from db.models import Users


async def get_user_by_telegram_id(telegram_id: int) -> Users:
    """"""
    with Session() as session:
        return session.query(Users).filter(Users.telegram_id == telegram_id).first()
