from django.contrib import admin

from books.admin.translate_model_form import get_translate_model_form
from books.models import BooksSentencesModel


@admin.register(BooksSentencesModel)
class BooksSentencesAdmin(admin.ModelAdmin):
    """BooksSentences admin."""

    form = get_translate_model_form()
    list_display = ('__str__', 'book', 'order')
    list_filter = ('book__level_en__title', )
    search_fields = ('text', )

    def get_readonly_fields(self, request, obj=None):
        return ['translation']
