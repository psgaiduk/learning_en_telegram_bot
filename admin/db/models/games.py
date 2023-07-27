from app import db


class Games(db.Model):
    """Model of games."""

    __tablename__ = 'games'

    game_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64))
    is_active = db.Column(db.Boolean, default=True)

    history = db.relationship('UsersGamesHistory', back_populates='game')
