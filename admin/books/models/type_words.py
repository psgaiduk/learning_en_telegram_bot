from django.db.models import AutoField, CharField, Model

from books.choices import TypeWord


class TypeWordsModel(Model):
    """Model of type of words."""

    type_word_id = AutoField(primary_key=True)
    title = CharField(max_length=128, choices=TypeWord.choices())

    def __str__(self) -> str:
        return f'{self.title}'

    class Meta:
        verbose_name = 'Type of word'
        verbose_name_plural = 'Types of words'
        db_table = 'type_words'
