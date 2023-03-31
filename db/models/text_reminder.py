from sqlalchemy import Column, Integer, String, Sequence

from db.models.base import Base


class TextReminder(Base):
    __tablename__ = 'text_reminders'

    id = Column(
        Integer,
        Sequence('text_reminders_id_seq'),
        primary_key=True,
        server_default=Sequence('text_reminders_id_seq').next_value(),
    )
    ru = Column(String, nullable=True)
    en = Column(String, nullable=True)
    fr = Column(String, nullable=True)
    es = Column(String, nullable=True)
    ge = Column(String, nullable=True)
    type_reminder = Column(String(length=32), nullable=True)
