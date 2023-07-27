from datetime import datetime

from app import db


class UsersHeroLevelsHistory(db.Model):
    """Model of history user's hero levels."""

    __tablename__ = 'users_hero_levels_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telegram_id = db.Column(db.ForeignKey('users.telegram_id'))
    hero_level_id = db.Column(db.ForeignKey('hero_levels.level_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    user = db.relationship('Users', back_populates='hero_levels_history', uselist=False)
    hero_level = db.relationship('HeroLevels', back_populates='heroes_levels_history', uselist=False)
