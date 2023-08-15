from sqlalchemy import Table, Column, Integer, ForeignKey

from database import Base


sentence_word_association = Table(
    'books_sentences_words', Base.metadata,
    Column('bookssentencesmodel_id', Integer, ForeignKey('books_sentences.sentence_id')),
    Column('wordsmodel_id', Integer, ForeignKey('words.word_id'))
)
