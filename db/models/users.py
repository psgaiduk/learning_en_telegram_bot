from sqlalchemy import BigInteger, Column, ForeignKey, VARCHAR

from db.models.base import Base
from settings import settings


class Users(Base):
    """Model of user."""

    if settings.environment == 'local':
        __tablename__ = '_local_users'
    else:
        __tablename__ = 'users'

    telegram_id = Column(BigInteger, primary_key=True)
    level_en_id = Column(ForeignKey('levels_en.level_en_id'))
    main_language_id = Column(ForeignKey('main_languages.main_language_id'))
    user_name = Column(VARCHAR(64))
    experience = Column(BigInteger, default=0)
    hero_level_id = Column(ForeignKey('hero_levels.level_id'))
    stage = Column(VARCHAR(64))
