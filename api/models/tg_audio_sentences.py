from sqlalchemy import BigInteger, Column, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


class TgAudioSentenceModel(Base):
    """Model of tg audio sentences."""

    __tablename__ = "tg_audio_sentences"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sentence_id = Column(
        BigInteger, ForeignKey("books_sentences.sentence_id", ondelete="CASCADE"), unique=True, nullable=False
    )
    audio_id = Column(Text, nullable=False)

    sentence = relationship("BooksSentences", back_populates="tg_audio_sentence", uselist=False)

    def __str__(self):
        return f"Книга {self.sentence.book.title}, Предложение {self.sentence.order}"
