from db.core import Session
from db.models import Users


def get_all_users() -> list[Users]:
    """"""
    with Session() as session:
        return session.query(Users).all()
