from db.core import Session
from db.models import Users


async def create_user(telegram_id: int, name: str):
    with Session() as session:
        new_user = Users(telegram_id=telegram_id, name=name, level=1)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
