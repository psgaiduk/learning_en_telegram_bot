from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from books.choices import TypeWord
from books.models import BooksModel, BooksSentencesModel, WordsModel, TypeWordsModel
from books.services import CreateWordsAndSentencesService
from telegram_users.choices import Language
from nlp_translate import translate_word, translate_text


@receiver(post_save, sender=BooksModel)
def create_words_and_sentences(sender, instance, created, **kwargs):
    if created:
        book_text = instance.text
        sentences = CreateWordsAndSentencesService().work(text=book_text)

        for sentence in sentences:
            words = WordsModel.objects.filter(word__in=sentence.words)
            new_words = set(sentence.words) - set(words.values_list('word', flat=True))
            type_word = TypeWordsModel.objects.get(title=TypeWord.word.value)
            for word in new_words:
                if len(word) < 3:
                    continue
                translates_word = {}
                for language_code, _ in Language.choices():
                    translates_word[language_code] = translate_word(word=word, language=language_code)
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
