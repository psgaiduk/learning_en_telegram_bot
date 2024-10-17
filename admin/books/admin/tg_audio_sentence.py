from django.contrib import admin

from books.models import TgAudioSentenceModel


@admin.register(TgAudioSentenceModel)
class TgAudioSentenceAdmin(admin.ModelAdmin):
    """Audio sentences in telegram admin."""

    list_display = ("__str__",)
