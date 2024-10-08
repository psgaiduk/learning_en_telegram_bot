from django.contrib import admin

from books.admin.translate_model_form import get_translate_model_form
from books.models import WordsModel


@admin.register(WordsModel)
class WordsAdmin(admin.ModelAdmin):
    """Words admin."""

    form = get_translate_model_form()
    list_display = ("__str__", "type_word", "part_of_speech", "translation")
    list_filter = ("type_word__title", "part_of_speech")
    search_fields = ("word",)

    def get_readonly_fields(self, request, obj=None):
        return ["translation"]
