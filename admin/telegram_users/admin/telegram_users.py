from django.contrib import admin

from telegram_users.models import TelegramUsersModel


@admin.register(TelegramUsersModel)
class TelegramUsersAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "level_en",
        "main_language",
        "hero_level",
        "stage",
        "experience",
    )
    list_filter = (
        "level_en__title",
        "main_language__title",
        "hero_level__title",
        "stage",
    )
    search_fields = ("telegram_id",)
