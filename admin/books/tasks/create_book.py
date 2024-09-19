from django.db.models import Q
from django_q.tasks import Chain
from loguru import logger

from ai_app import AISDK
from books.models import BooksModel, BooksSentencesModel, TensesModel
from books.services import CreateWordsForSentenceService


def create_book_task(book_id: int) -> None:
    """
    Create books.

    :param book_id: book id.
    """
    logger.info(f"Create book {book_id}")
    instance = BooksModel.objects.get(book_id=book_id)
    logger.debug(f"Book {instance.book_id} - {instance.title}")
    logger.debug(f"Book text {instance.text}")
    chain = Chain(cached=True)
    logger.debug(f"Chain {chain}")
    sentences = instance.text.split("\n")
    sentences = [sentence for sentence in sentences if sentence and "---" in sentence]
    logger.debug(f"Sentences {sentences}")
    for index, sentence in enumerate(sentences):
        chain.append(create_sentences, instance, sentence, index)
    chain.run()


def create_sentences(instance: BooksModel, sentence: str, index: int) -> None:
    """
    Translate and add sentence.

    :param instance: book instance.
    :param sentence: sentence string.
    :param index: index of sentence.
    """
    sentence_data = sentence.split("---")
    english_sentence = sentence_data[0].strip()
    logger.debug(f"English sentence {english_sentence}")
    russian_sentence = sentence_data[1].strip()
    logger.debug(f"Russian sentence {russian_sentence}")
    english_words_with_transcription = sentence_data[2]
    logger.debug(f"Words with transcriptions {english_words_with_transcription}")
    words_ids = CreateWordsForSentenceService(raw_words=english_words_with_transcription).work()
    logger.debug(f"Words ids: {words_ids}")
    sentence_tenses: list = sentence_data[3].strip().split(", ")
    logger.debug(f"Sentence times {sentence_tenses}")

    AISDK().create_audio_file(
        sentence=english_sentence, file_name=f"{instance.book_id} - {index}", level_order=instance.level_en.order
    )
    tenses = TensesModel.objects.filter(Q(name__in=sentence_tenses))

    book_sentence, created = BooksSentencesModel.objects.update_or_create(
        book=instance,
        order=index + 1,
        defaults={
            "text": english_sentence,
            "translation": {"ru": russian_sentence},
        },
    )

    book_sentence.words.set(words_ids)
    book_sentence.tenses.set(tenses)
