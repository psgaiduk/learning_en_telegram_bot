from django.db.models import CharField, IntegerField, Model

from telegram_users.choices import LevelEn


class LevelsEnModel(Model):
    """Model of levels en."""
    title = CharField(max_length=64, choices=LevelEn.choices())
    order = IntegerField()

    def __str__(self) -> str:
        return f'{self.title} - {self.get_title_display()}'

    class Meta:
        db_table = 'levels_en'
        ordering = ['order']
