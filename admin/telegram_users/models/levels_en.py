from django.db.models import CharField, IntegerField, Model

from telegram_users.choices import LevelEn


class LevelsEnModel(Model):
    """Model of levels en."""
    title = CharField(max_length=64, choices=LevelEn.choices())
    description = CharField(max_length=128)
    order = IntegerField()

    def __str__(self) -> str:
        return f'{self.title} - {self.description}'

    class Meta:
        verbose_name = 'English level'
        verbose_name_plural = 'English levels'
        db_table = 'levels_en'
        ordering = ['order']
