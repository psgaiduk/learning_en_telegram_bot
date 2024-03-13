from django.db.models import Q
from django_q.tasks import Chain
from loguru import logger

from ai_app import AISDK
from books.models import BooksModel, BooksSentencesModel, TensesModel, WordsModel
from nlp_translate import translate_text


def create_book_task(book_id: int) -> None:
    """
    Create books.

    :param book_id: book id.
    """
    logger.info(f'Create book {book_id}')
    instance = BooksModel.objects.get(book_id=book_id)
    logger.debug(f'Book {instance.book_id} - {instance.title}')
    logger.debug(f'Book text {instance.text}')
    chain = Chain(cached=True)
    logger.debug(f'Chain {chain}')
    sentences = instance.text.split('\n')
    sentences = [sentence for sentence in sentences if sentence and '---' in sentence]
    logger.debug(f'Sentences {sentences}')
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
    sentence_data = sentence.split('---')
    english_sentence = sentence_data[0].strip()
    logger.debug(f'English sentence {english_sentence}')
    russian_sentence = sentence_data[1].strip()
    logger.debug(f'Russian sentence {russian_sentence}')
    english_words = sentence_data[2].replace('.', '').split('; ')
    english_words = set([word.strip().lower() for word in english_words])
    logger.debug(f'Words {english_words}')
    sentence_tenses: list = sentence_data[3].strip().split(', ')
    logger.debug(f'Sentence times {sentence_tenses}')

    AISDK().create_audio_file(sentence=english_sentence, file_name=f'{instance.book_id} - {index}')

    logger.debug(f'English words {english_words}')
    words_in_database = WordsModel.objects.filter(word__in=english_words)
    logger.debug(f'Words in database {words_in_database}')
    new_english_words = english_words - set(words_in_database.values_list('word', flat=True))
    logger.debug(f'Words for translate {new_english_words}')
    if new_english_words:
        words_for_translate = '; '.join(english_words)
        translate_words = translate_text(text_on_en=words_for_translate, language='ru').split('; ')
        logger.debug(f'Translates words {translate_words}')

        for index_word, word in enumerate(english_words):
            if word not in new_english_words:
                continue
            translate_word = translate_words[index_word].lower()
            logger.debug(f'English word {word} - {translate_word}')
            type_word_id = 1
            if ' ' in word:
                type_word_id = 2
            WordsModel.objects.create(word=word, translation={'ru': translate_word}, type_word_id=type_word_id)

    words = WordsModel.objects.filter(Q(word__in=english_words))
    tenses = TensesModel.objects.filter(Q(name__in=sentence_tenses))

    book_sentence, created = BooksSentencesModel.objects.update_or_create(
        book=instance,
        order=index + 1,
        defaults={
            'text': english_sentence,
            'translation': {'ru': russian_sentence},
        }
    )

    book_sentence.words.set(words)
    book_sentence.tenses.set(tenses)
