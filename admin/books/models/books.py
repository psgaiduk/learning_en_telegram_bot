from django.db.models import AutoField, CASCADE, CharField, ForeignKey, Model, TextField


class BooksModel(Model):
    """Model of books."""

    book_id = AutoField(primary_key=True)
    title = CharField(max_length=128)
    level_en = ForeignKey('telegram_users.LevelsEnModel', on_delete=CASCADE)
    author = CharField(max_length=128)
    text = TextField()
    previous_book = ForeignKey('self', on_delete=CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        db_table = 'books'
