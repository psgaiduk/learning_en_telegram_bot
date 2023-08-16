from datetime import datetime

from django.db.models import BooleanField, CASCADE, DateTimeField, ForeignKey, JSONField, Model

from telegram_users.models.telegram_users import TelegramUsersModel
from books.models import BooksSentencesModel


class UsersBooksSentencesHistoryModel(Model):
    """Model of history user's books sentences."""

    telegram_user = ForeignKey(TelegramUsersModel, on_delete=CASCADE)
    sentence = ForeignKey(BooksSentencesModel, on_delete=CASCADE)
    check_words = JSONField(blank=True, null=True)
    is_read = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return f'{self.telegram_user.telegram_id} - {self.sentence.book.title} - {self.sentence.sentence_id}'

    class Meta:
        db_table = 'users_books_sentences_history'
        verbose_name = 'User\'s books sentences history'
        verbose_name_plural = 'Users\' books sentences history'
