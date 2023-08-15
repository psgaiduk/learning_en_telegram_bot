from django.db.models import AutoField, CASCADE, TextField, JSONField, IntegerField, ForeignKey, Model, ManyToManyField

from models.books import BooksModel
from models.words import WordsModel


class BooksSentencesModel(Model):
    """Model of books sentences."""

    sentence_id = AutoField(primary_key=True)
    book = ForeignKey(BooksModel, on_delete=CASCADE, related_name='books_sentences')
    order = IntegerField()
    text = TextField()
    translation = JSONField(null=True, blank=True)
    words = ManyToManyField(WordsModel, related_name='books_sentences')

    def __str__(self):
        return f'Book {self.book.title}, Sentence {self.order}'

    class Meta:
        verbose_name = 'Sentence'
        verbose_name_plural = 'Sentences'
        db_table = 'books_sentences'
