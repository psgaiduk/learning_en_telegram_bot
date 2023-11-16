from django.db.models import Q
from django_q.tasks import Chain

from books.choices import TypeWord
from books.dto import SentenceDTO
from books.models import BooksModel, BooksSentencesModel, WordsModel, TypeWordsModel
from books.services import CreateWordsAndSentencesService
from telegram_users.choices import Language
from nlp_translate import translate_text


def create_book_task(book_id: int) -> None:
    """Create books."""
    instance = BooksModel.objects.get(book_id=book_id)
    book_text = instance.text
    sentences = CreateWordsAndSentencesService().work(text=book_text)
    chain = Chain(cached=True)

    for sentence in sentences:
        chain.append(create_sentence, sentence, instance)
    
    chain.run()


def create_sentence(sentence: SentenceDTO, instance: BooksModel) -> None:
    """Translate and add sentence."""
    words = WordsModel.objects.filter(word__in=sentence.words)
    new_words = set(sentence.words) - set(words.values_list('word', flat=True))
    type_word = TypeWordsModel.objects.get(title=TypeWord.word.value)
    for word in new_words:
        if len(word) < 3:
            continue
        translates_word = {}
        for language_code, _ in Language.choices():
            translates_word[language_code] = translate_text(text_on_en=word, language=language_code)
        WordsModel.objects.create(word=word, translation=translates_word, type_word=type_word)

    translates_sentence = {}
    for language_code, _ in Language.choices():
        translate_sentence = translate_text(text_on_en=sentence.text, language=language_code)
        translates_sentence[language_code] = translate_sentence

    words = WordsModel.objects.filter(
        Q(word__in=sentence.words) |
        Q(word__in=sentence.idiomatic_expression) |
        Q(word__in=sentence.phrase_verb)
    )

    book_sentence, created = BooksSentencesModel.objects.update_or_create(
        book=instance,
        order=sentence.index,
        defaults={
            'text': sentence.text,
            'translation': translates_sentence,
        }
    )

    book_sentence.words.set(words)
