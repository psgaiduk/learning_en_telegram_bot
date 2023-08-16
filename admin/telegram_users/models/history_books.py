from django.db.models import Model, ForeignKey, DateTimeField, CASCADE

from books.models import BooksModel
from telegram_users.models.telegram_users import TelegramUsersModel


class UsersBooksHistoryModel(Model):
    telegram_user = ForeignKey(TelegramUsersModel, on_delete=CASCADE)
    book = ForeignKey(BooksModel, on_delete=CASCADE)
    start_read = DateTimeField(auto_now_add=True)
    end_read = DateTimeField(null=True, default=None)
    
    def __str__(self) -> str:
        return f'{self.telegram_user.name} - {self.book.title}'

    class Meta:
        db_table = 'users_books_history'
        verbose_name = 'User\'s book history'
        verbose_name_plural = 'Users\' book history'
