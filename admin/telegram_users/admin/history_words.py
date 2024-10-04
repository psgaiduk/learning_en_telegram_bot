from django.contrib import admin

from telegram_users.models import UsersWordsHistoryModel


@admin.register(UsersWordsHistoryModel)
class UsersWordsHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "telegram_user",
        "is_known",
        "count_view",
        "correct_answers",
        "incorrect_answers",
    )
    list_filter = ("is_known",)
    search_fields = ("telegram_user__telegram_id", "word__word")
