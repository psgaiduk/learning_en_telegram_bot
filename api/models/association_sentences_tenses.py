from sqlalchemy import Table, Column, Integer, ForeignKey

from database import Base


sentence_tenses_association = Table(
    'books_sentences_tenses', Base.metadata,
    Column('bookssentencesmodel_id', Integer, ForeignKey('books_sentences.sentence_id')),
    Column('tensesmodel_id', Integer, ForeignKey('tenses.id'))
)
