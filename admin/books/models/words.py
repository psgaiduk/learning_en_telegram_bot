from django.db.models import AutoField, CASCADE, CharField, ForeignKey, JSONField, Model


class WordsModel(Model):
    """Model of words."""

    word_id = AutoField(primary_key=True)
    type_word = ForeignKey('TypeWordsModel', on_delete=CASCADE)
    word = CharField(max_length=128, )
    translation = JSONField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.word}'

    class Meta:
        db_table = 'words'
        verbose_name = 'Word'
        verbose_name_plural = 'Words'
