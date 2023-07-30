from django.contrib import admin

from books.models import WordsModel


@admin.register(WordsModel)
class WordsAdmin(admin.ModelAdmin):
    """Words admin."""

    list_display = ('__str__', 'type_word')
    list_filter = ('type_word__title', )
    search_fields = ('word', )
