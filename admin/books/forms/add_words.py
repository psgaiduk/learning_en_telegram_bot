from django import forms

from books.choices import TypeWord


class WordsUploadForm(forms.Form):
    words = forms.CharField(widget=forms.Textarea, help_text="Add words here separated by a new line")
    type_words = forms.ChoiceField(choices=TypeWord.choices(), help_text="Type of words")
