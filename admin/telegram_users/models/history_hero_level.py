from datetime import datetime

from django.db.models import CASCADE, DateTimeField, ForeignKey, Model

from telegram_users.models.telegram_users import TelegramUsersModel
from telegram_users.models.hero_levels import HeroLevelsModel


class UsersHeroLevelsHistoryModel(Model):
    """Users hero levels history model."""

    telegram_user = ForeignKey(TelegramUsersModel, on_delete=CASCADE)
    hero_level = ForeignKey(HeroLevelsModel, on_delete=CASCADE)
    created_at = DateTimeField(default=datetime.utcnow)

    class Meta:
        db_table = 'users_hero_levels_history'
        verbose_name = 'Users\' history hero levels'
        verbose_name_plural = 'Users\' history hero levels'

    def __str__(self):
        return f'{self.telegram_user.telegram_id} - {self.hero_level.title}'
