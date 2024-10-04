from django.contrib import admin

from telegram_users.models import UsersBooksSentencesHistoryModel


@admin.register(UsersBooksSentencesHistoryModel)
class UsersBooksSentencesHistoryAdmin(admin.ModelAdmin):
    list_display = ("__str__", "telegram_user", "is_read")
    list_filter = ("sentence__book__level_en__title", "is_read")
    search_fields = ("telegram_user__telegram_id", "sentence__book__title")
