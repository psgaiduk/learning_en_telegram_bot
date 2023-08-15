from sqlalchemy import Table, Column, Integer, ForeignKey

from database import Base


sentence_word_association = Table(
    'sentence_word_association', Base.metadata,
    Column('sentence_id', Integer, ForeignKey('books_sentences.sentence_id')),
    Column('word_id', Integer, ForeignKey('words.word_id'))
)
