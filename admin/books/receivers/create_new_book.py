from django.db.models.signals import post_save
from django.dispatch import receiver

from books.models import BooksModel, BooksSentencesModel, WordsModel
from books.services import CreateWordsAndSentencesService


@receiver(post_save, sender=BooksModel)
def create_words_and_sentences(sender, instance, created, **kwargs):
    print('create_words_and_sentences')
    if not kwargs.get('created', False):
        instance.books_sentences.all().delete()

    book_text = instance.text
    sentences = CreateWordsAndSentencesService().work(text=book_text)
    print(sentences)


    # for i, sentence_text in enumerate(sentences):
    #     # sentence = BooksSentencesModel.objects.create(
    #     #     book=instance,
    #     #     order=i + 1,
    #     #     text=sentence_text,
    #     # )
    #
    #     words = sentence_text.split()
    #
    #     for word_text in words:
    #         word, _ = WordsModel.objects.get_or_create(word=word_text)
    #         sentence.words.add(word)
