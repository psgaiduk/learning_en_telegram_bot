from django.contrib import admin

from telegram_users.models import LevelsEnModel


@admin.register(LevelsEnModel)
class LevelsEnAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
