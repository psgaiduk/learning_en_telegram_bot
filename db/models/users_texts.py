from sqlalchemy import Column, Date, func, String
from sqlalchemy import Table
from sqlalchemy import ForeignKey

from db.models.base import Base


users_texts = Table(
    'users_texts',
    Base.metadata,
    Column('date', Date, server_default=func.now()),
    Column('language', String),
    Column('user_telegram_id', ForeignKey('users.telegram_id'), primary_key=True),
    Column('text_id', ForeignKey('texts.id'), primary_key=True),
)
