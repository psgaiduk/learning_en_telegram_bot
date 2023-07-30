from django import forms
from django.contrib import admin

from books.models import WordsModel
from telegram_users.choices import Language


def get_word_translate_model_form():
    fields = {
        lang_choice[0]: forms.CharField(label=lang_choice[1], required=False)
        for lang_choice in Language.choices()
    }

    class WordTranslateModelForm(forms.ModelForm):
        class Meta:
            model = WordsModel
            fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            instance = kwargs.get('instance')
            if instance and instance.translation:
                for lang_choice in Language.choices():
                    field_name = lang_choice[0]
                    self.fields[field_name].initial = instance.translation.get(field_name, '')

        def save(self, commit=True):
            instance = super().save(commit=False)
            instance.translation = {field_name: self.cleaned_data[field_name] for field_name, _ in Language.choices()}
            if commit:
                instance.save()
            return instance

    return type('WordTranslateModelForm', (WordTranslateModelForm,), fields)


@admin.register(WordsModel)
class WordsAdmin(admin.ModelAdmin):
    """Words admin."""

    form = get_word_translate_model_form()
    list_display = ('__str__', 'type_word')
    list_filter = ('type_word__title', )
    search_fields = ('word', )

    def get_readonly_fields(self, request, obj=None):
        return ['translation']
