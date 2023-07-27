from app import db


class MainLanguages(db.Model):
    """Model of main languages."""

    __tablename__ = 'main_languages'

    main_language_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64))

    users = db.relationship('Users', back_populates='main_language')
