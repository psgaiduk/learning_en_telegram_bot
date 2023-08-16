from django.contrib import admin

from telegram_users.models import UsersHeroLevelsHistoryModel


@admin.register(UsersHeroLevelsHistoryModel)
class UsersHeroLevelsHistoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'telegram_user', 'hero_level', 'created_at')
    list_filter = ('hero_level', )
    search_fields = ('telegram_user__telegram_id', )
