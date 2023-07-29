from django.contrib import admin

from books.models import BooksModel


@admin.register(BooksModel)
class BooksAdmin(admin.ModelAdmin):
    """Books admin."""

    list_display = ('__str__', 'level_en', 'author')
    list_filter = ('level_en__title', 'author')
    search_fields = ('author', 'title')
