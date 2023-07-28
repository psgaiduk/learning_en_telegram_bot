from django.contrib import admin

from telegram_users.models import HeroLevelsModel


@admin.register(HeroLevelsModel)
class HeroLevelsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'need_experience', 'count_sentences', 'count_games', 'order')
