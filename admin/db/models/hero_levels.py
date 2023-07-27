from app import db


class HeroLevels(db.Model):
    """Model of hero levels."""

    __tablename__ = 'hero_levels'

    level_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64))
    need_experience = db.Column(db.BigInteger)
    count_sentences = db.Column(db.Integer)
    count_games = db.Column(db.Integer)
    order = db.Column(db.Integer)

    users = db.relationship('Users', back_populates='hero_level')
    heroes_levels_history = db.relationship('UsersHeroLevelsHistory', back_populates='hero_level')
