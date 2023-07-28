from django.contrib import admin

from telegram_users.models import MainLanguagesModel


@admin.register(MainLanguagesModel)
class MainLanguagesAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
