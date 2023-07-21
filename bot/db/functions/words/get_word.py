from random import choice

from sqlalchemy.sql.expression import func

from db.core import Session
from db.models import Word


def get_random_word_by_symbols(symbols: int) -> Word:
    """Get one random word from database by count of symbols."""
    with Session() as session:
        words = session.query(Word).filter(func.char_length(Word.english) == symbols).all()
        return choice(words)
