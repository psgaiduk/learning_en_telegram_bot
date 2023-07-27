from django.db.models import CharField, Model


class MainLanguagesModel(Model):
    """Model of main languages."""
    title = CharField(max_length=64)

    class Meta:
        db_table = 'main_languages'
