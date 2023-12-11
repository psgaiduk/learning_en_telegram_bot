from django.db.models import Q
from django_q.tasks import Chain
from loguru import logger

from ai_app import AISDK
from books.dto import SentenceDTO
from books.models import BooksModel, BooksSentencesModel, WordsModel, TypeWordsModel
from books.services import CreateWordsAndSentencesService
from telegram_users.choices import Language
from nlp_translate import translate_text


def create_book_task(book_id: int) -> None:
    """Create books."""
    logger.info(f'Create book {book_id}')
    instance = BooksModel.objects.get(book_id=book_id)
    logger.debug(f'Book {instance.book_id} - {instance.title}')
    logger.debug(f'Book text {instance.text}')
    sentences = CreateWordsAndSentencesService(book=instance).work()
    logger.debug(f'Sentences {sentences}')
    chain = Chain(cached=True)
    logger.debug(f'Chain {chain}')

    for sentence in sentences:
        logger.debug(f'Sentence {sentence}')
        chain.append(create_sentence, sentence, instance)

    logger.debug(f'Chain {chain}')
    chain.run()


def create_sentence(sentence: SentenceDTO, instance: BooksModel) -> None:
    """Translate and add sentence."""
    words_from_ai = AISDK().get_words(sentence=sentence.text, english_level=instance.level_en.title)
    AISDK().create_audio_file(sentence=sentence.text, file_name=f'{instance.book_id} - {sentence.index}')
    words_by_type = {1: [], 2: [], 3: []}

    for word in words_from_ai:
        if '- 1' in word:
            words_by_type[3].append(word.replace(' - 1', '').strip())
        elif '- 2' in word:
            words_by_type[2].append(word.replace(' - 2', '').strip())
        elif '- 3' in word:
            words_by_type[1].append(word.replace(' - 3', '').strip())

    all_words = sum(words_by_type.values(), [])
    words = WordsModel.objects.filter(word__in=all_words)
    new_words = set(all_words) - set(words.values_list('word', flat=True))
    for type_word_id, words in words_by_type.items():
        type_word = TypeWordsModel.objects.get(type_word_id=type_word_id)
        for word in words:
            if len(word) < 3 or word not in new_words:
                continue
            translates_word = {}
            for language_code, _ in Language.choices():
                translates_word[language_code] = translate_text(text_on_en=word, language=language_code)
            WordsModel.objects.create(word=word, translation=translates_word, type_word=type_word)

    translates_sentence = {}
    for language_code, _ in Language.choices():
        translate_sentence = translate_text(text_on_en=sentence.text, language=language_code)
        translates_sentence[language_code] = translate_sentence

    words = WordsModel.objects.filter(Q(word__in=all_words))

    book_sentence, created = BooksSentencesModel.objects.update_or_create(
        book=instance,
        order=sentence.index,
        defaults={
            'text': sentence.text,
            'translation': translates_sentence,
        }
    )

    book_sentence.words.set(words)
