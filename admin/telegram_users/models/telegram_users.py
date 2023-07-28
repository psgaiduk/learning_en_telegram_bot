from django.db.models import BigIntegerField, CASCADE, CharField, ForeignKey, Model, SET_NULL


class TelegramUsersModel(Model):
    """Model of telegram users."""

    telegram_id = BigIntegerField(primary_key=True)
    level_en = ForeignKey('LevelsEnModel', on_delete=SET_NULL, null=True)
    main_language = ForeignKey('MainLanguagesModel', on_delete=CASCADE)
    user_name = CharField(max_length=64, null=True, blank=True)
    experience = BigIntegerField(default=0)
    hero_level = ForeignKey('HeroLevelsModel', on_delete=CASCADE)
    previous_stage = CharField(max_length=64, null=True, blank=True)
    stage = CharField(max_length=64, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.telegram_id} - {self.user_name}'

    class Meta:
        verbose_name = 'Telegram user'
        verbose_name_plural = 'Telegram users'
        db_table = 'telegram_users'
