from django.contrib import messages
from django.shortcuts import redirect, render

from books.forms import WordsUploadForm
from books.processes import AddNewWordsProcess
from telegram_users.choices import Language


def upload_words_view(request):
    if request.method == 'POST':
        form = WordsUploadForm(request.POST)
        if form.is_valid():
            bad_words = []
            words = []
            words_list = form.cleaned_data['words'].split('\n')
            for word in words_list:

                if ' - ' not in word:
                    bad_words.append(word)
                    continue

                word = word.replace(' - ', '***').replace('"', '')
                word_with_translate = word.split('***')
                word_dict = {'word': word_with_translate.pop(0), 'translate': {}}
                
                if len(word_with_translate) != len(Language.choices()):
                    bad_words.append(word)
                    continue

                for index, language in enumerate(Language.choices()):
                    word_translate = word_with_translate[index]
                    word_dict['translate'][language[0]] = word_translate
                words.append(word_dict)
            _add_new_words_process = AddNewWordsProcess()
            _add_new_words_process(words=words, type_words=form.cleaned_data['type_words'])
            messages.error(request, f'Следующие слова не были добавлены: {bad_words}')
            messages.success(request, 'Слова были успешно добавлены!')
            return redirect('/admin/')
    else:
        form = WordsUploadForm()

    return render(request, 'admin/add_words_form.html', {'form': form})
