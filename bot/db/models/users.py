from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from db.models.base import Base


class Users(Base):
    """Model of user."""

    __tablename__ = 'users'

    telegram_id = Column(BigInteger, primary_key=True)
    level_en_id = Column(ForeignKey('levels_en.level_en_id'), nullable=True)
    main_language_id = Column(ForeignKey('main_languages.main_language_id'))
    user_name = Column(String(64), nullable=True)
    experience = Column(BigInteger, default=0)
    hero_level_id = Column(ForeignKey('hero_levels.level_id'))
    previous_stage = Column(String(64), nullable=True)
    stage = Column(String(64), nullable=True)

    games = relationship('UsersGamesHistory', back_populates='user')
    referrals = relationship('UsersReferrals', back_populates='user')
    subscribes = relationship('UsersSubscribes', back_populates='user')
    hero_levels_history = relationship('UsersHeroLevelsHistory', back_populates='user')
    charges_history = relationship('UsersChargesHistory', back_populates='user')
    books_history = relationship('UsersBooksHistory', back_populates='user')
    books_sentences_history = relationship('UsersBooksSentencesHistory', back_populates='user')
    achievements_history = relationship('UsersAchievementsHistory', back_populates='user')
    grammar_exercises_history = relationship('UsersGrammarExercisesHistory', back_populates='user')
    words_history = relationship('UsersWordsHistory', back_populates='user')

    level_en = relationship('LevelsEn', back_populates='users', uselist=False)
    hero_level = relationship('HeroLevels', back_populates='users', uselist=False)
    main_language = relationship('MainLanguages', back_populates='users', uselist=False)
