from django.contrib import admin

from telegram_users.models import UsersBooksHistoryModel


@admin.register(UsersBooksHistoryModel)
class UsersBooksHistoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'book', 'start_read', 'end_read')
    list_filter = ('book__level_en__title', )
    search_fields = ('telegram_user__telegram_id', 'book__title')
