from django.contrib import admin

from books.models import TypeWordsModel


@admin.register(TypeWordsModel)
class TypeWordsAdmin(admin.ModelAdmin):
    """TypeWords admin."""

    list_display = ("__str__",)
