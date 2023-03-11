from sqlalchemy import Column, Date, String, Integer
from sqlalchemy import Table
from sqlalchemy import ForeignKey

from db.models.base import Base


users_texts = Table(
    'users_texts',
    Base.metadata,
    Column('id', Integer, index=True, primary_key=True),
    Column('date', Date),
    Column('language', String),
    Column('user_telegram_id', ForeignKey('users.telegram_id')),
    Column('text_id', ForeignKey('texts.id')),
)
