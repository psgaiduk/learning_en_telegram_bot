from django.db.models import AutoField, CASCADE, CharField, ForeignKey, JSONField, IntegerField, Model


class WordsModel(Model):
    """Model of words."""

    word_id = AutoField(primary_key=True)
    type_word_id = ForeignKey('TypeWordsModel', on_delete=CASCADE)
    word = CharField(max_length=128)
    translation = JSONField()

    def __str__(self) -> str:
        return f'{self.word}'

    class Meta:
        db_table = 'words'
        verbose_name = 'Word'
        verbose_name_plural = 'Words'
