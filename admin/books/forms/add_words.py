from django import forms


class WordsUploadForm(forms.Form):
    words = forms.CharField(widget=forms.Textarea, help_text="Add words here separated by a new line")
    type_words = forms.CharField(max_length=200, help_text="Type of words")
