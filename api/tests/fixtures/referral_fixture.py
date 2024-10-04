from pytest import fixture

from tests.connect_db import db_session
from models import Users, UsersReferrals
from tests.fixtures.telegram_users_fixture import telegram_users_mock


@fixture
def referrals_fixture(telegram_users_mock):
    with db_session() as db:
        telegram_users = db.query(Users).all()

        first_telegram_user = telegram_users.pop(0)
        second_telegram_user = telegram_users.pop(0)
        third_telegram_user = telegram_users.pop(0)

        referral = {
            "telegram_id": second_telegram_user.telegram_id,
            "friend_telegram_id": third_telegram_user.telegram_id,
        }

        db.add(UsersReferrals(**referral))

        for telegram_user in telegram_users:
            referral = {
                "telegram_id": first_telegram_user.telegram_id,
                "friend_telegram_id": telegram_user.telegram_id,
            }

            db.add(UsersReferrals(**referral))

        db.commit()
