from app import db


class Users(db.Model):
    """Model of user."""

    __tablename__ = 'users'

    telegram_id = db.Column(db.BigInteger, primary_key=True)
    level_en_id = db.Column(db.ForeignKey('levels_en.level_en_id'), nullable=True)
    main_language_id = db.Column(db.ForeignKey('main_languages.main_language_id'))
    user_name = db.Column(db.String(64), nullable=True)
    experience = db.Column(db.BigInteger, default=0)
    hero_level_id = db.Column(db.ForeignKey('hero_levels.level_id'))
    previous_stage = db.Column(db.String(64), nullable=True)
    stage = db.Column(db.String(64), nullable=True)

    referrals = db.relationship('UsersReferrals', back_populates='user',  foreign_keys='UsersReferrals.telegram_id')
    friends = db.relationship(
        'UsersReferrals', back_populates='friend',  foreign_keys='UsersReferrals.friend_telegram_id')
    subscribes = db.relationship('UsersSubscribes', back_populates='user')
    hero_levels_history = db.relationship('UsersHeroLevelsHistory', back_populates='user')
    charges_history = db.relationship('UsersChargesHistory', back_populates='user')
    books_history = db.relationship('UsersBooksHistory', back_populates='user')
    books_sentences_history = db.relationship('UsersBooksSentencesHistory', back_populates='user')
    achievements_history = db.relationship('UsersAchievementsHistory', back_populates='user')
    grammar_exercises_history = db.relationship('UsersGrammarExercisesHistory', back_populates='user')
    words_history = db.relationship('UsersWordsHistory', back_populates='user')
    games_history = db.relationship('UsersGamesHistory', back_populates='user')

    level_en = db.relationship('LevelsEn', back_populates='users', uselist=False)
    hero_level = db.relationship('HeroLevels', back_populates='users', uselist=False)
    main_language = db.relationship('MainLanguages', back_populates='users', uselist=False)
