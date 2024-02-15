from django.db.models import AutoField, CharField, Model, TextField


class TensesModel(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=64)
    short_description = TextField()
    full_description = TextField()
    image_telegram_id = TextField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'tenses'
        verbose_name = 'tenses'
        verbose_name_plural = 'tenses'
