from datetime import datetime

from django.db.models import (
    BooleanField,
    CASCADE,
    DateTimeField,
    FloatField,
    ForeignKey,
    Model,
    PositiveIntegerField,
)

from telegram_users.models.telegram_users import TelegramUsersModel
from books.models.words import WordsModel


class UsersWordsHistoryModel(Model):
    """Users' words history model."""

    telegram_user = ForeignKey(TelegramUsersModel, on_delete=CASCADE)
    word = ForeignKey(WordsModel, on_delete=CASCADE)
    is_known = BooleanField(default=False)
    count_view = PositiveIntegerField(default=0)
    correct_answers = PositiveIntegerField(default=0)
    incorrect_answers = PositiveIntegerField(default=0)
    correct_answers_in_row = PositiveIntegerField(default=0)
    increase_factor = FloatField(default=2.0)
    interval_repeat = PositiveIntegerField(default=600)
    repeat_datetime = DateTimeField(default=datetime.utcnow)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    class Meta:
        db_table = "users_words_history"
        verbose_name = "Users' history words"
        verbose_name_plural = "Users' history words"

    def __str__(self):
        return f"{self.telegram_user.telegram_id} - {self.word.word}"
