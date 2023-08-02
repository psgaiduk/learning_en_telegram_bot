from django.shortcuts import render


from books.forms import WordsUploadForm


def upload_words_view(request):
    if request.method == 'POST':
        form = WordsUploadForm(request.POST)
        if form.is_valid():
            words = []
            words_list = form.cleaned_data['words'].split('\n')
            for word in words_list:
                print(word)
            # _add_new_words_process = AddNewWordsProcess()
            # _add_new_words_process(words=words, type_words=form.cleaned_data['type_words'])
            # здесь вы можете добавить сообщение об успехе или перенаправление
    else:
        form = WordsUploadForm()

    return render(request, 'admin/add_words_form.html', {'form': form})
