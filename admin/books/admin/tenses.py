from django.contrib import admin

from books.models import TensesModel


@admin.register(TensesModel)
class TensesAdmin(admin.ModelAdmin):
    """Tenses admin."""

    list_display = ('__str__', )
