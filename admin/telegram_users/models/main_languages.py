from django.db.models import CharField, Model

from telegram_users.choices import Language


class MainLanguagesModel(Model):
    """Model of main languages."""
    title = CharField(max_length=64, choices=Language.choices())
    description = CharField(max_length=128)

    def __str__(self) -> str:
        return f'{self.description}'

    class Meta:
        verbose_name = 'Main language'
        verbose_name_plural = 'Main languages'
        db_table = 'main_languages'
