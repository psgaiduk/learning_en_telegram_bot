from sqlalchemy import BigInteger, Column, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.association_sentences_tenses import sentence_tenses_association
from models.association_sentenses_words import sentence_word_association
from database import Base


class BooksSentences(Base):
    """Model of books sentences."""

    __tablename__ = "books_sentences"

    sentence_id = Column(BigInteger, primary_key=True, autoincrement=True)
    book_id = Column(ForeignKey("books.book_id"))
    order = Column(Integer)
    text = Column(JSON)
    translation = Column(JSON)

    book = relationship("BooksModel", back_populates="books_sentences", uselist=False)
    words = relationship("Words", secondary=sentence_word_association, back_populates="sentences")
    tenses = relationship("Tenses", secondary=sentence_tenses_association, back_populates="sentences")
    users_books_sentences_history = relationship("UsersBooksSentencesHistory", back_populates="sentence")
    tg_audio_sentence = relationship("TgAudioSentenceModel", back_populates="sentence", uselist=False)
