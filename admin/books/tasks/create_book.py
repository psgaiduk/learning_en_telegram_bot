from django.db.models import Q
from django_q.tasks import Chain
from loguru import logger
from nltk import sent_tokenize

from ai_app import AISDK
from books.models import BooksModel, BooksSentencesModel, WordsModel, TypeWordsModel


global_index = 1


def create_book_task(book_id: int) -> None:
    """Create books."""
    logger.info(f'Create book {book_id}')
    instance = BooksModel.objects.get(book_id=book_id)
    logger.debug(f'Book {instance.book_id} - {instance.title}')
    logger.debug(f'Book text {instance.text}')
    chain = Chain(cached=True)
    logger.debug(f'Chain {chain}')
    sentences = sent_tokenize(instance.text)
    logger.debug(f'Sentences {sentences}')
    chunk = ""
    for sentence in sentences:
        if len(chunk) + len(sentence) <= 700:
            chunk += " " + sentence
        else:
            chain.append(create_sentences, instance, chunk.strip())
            logger.debug(f'Add sentence to chain {chunk.strip()}')
            chunk = sentence

    if chunk:
        logger.debug('Last chunk')
        chain.append(create_sentences, instance, chunk.strip())
        logger.debug(f'Add sentence to chain {chunk.strip()}')

    chain.run()


def create_sentences(instance: BooksModel, text: str) -> None:
    """Translate and add sentence."""
    global global_index
    text_data = AISDK().translate_and_analyse(text=text)
    logger.debug(f'Text data {text_data}')
    sentences = text_data.split('\n')
    sentences = [sentence for sentence in sentences if sentence and '---' in sentence]
    logger.debug(f'Sentences {sentences}')
    type_word = TypeWordsModel.objects.get(type_word_id=1)
    type_phrase = TypeWordsModel.objects.get(type_word_id=2)
    for sentence in sentences:
        sentence_data = sentence.split('---')
        english_sentence = sentence_data[0].strip()
        logger.debug(f'English sentence {english_sentence}')
        russian_sentence = sentence_data[1].strip()
        logger.debug(f'Russian sentence {russian_sentence}')
        words_with_translate = sentence_data[2].replace('.', '').strip().split('; ')
        logger.debug(f'Words with translate {words_with_translate}')
        sentence_times = sentence_data[3].strip()
        logger.debug(f'Sentence times {sentence_times}')
        description_time = sentence_data[4].strip()
        logger.debug(f'Description time {description_time}')

        AISDK().create_audio_file(sentence=english_sentence, file_name=f'{instance.book_id} - {global_index}')

        all_words = [word.split(': ')[0] for word in words_with_translate]
        logger.debug(f'All words {all_words}')

        words = WordsModel.objects.filter(word__in=all_words)
        new_words = set(all_words) - set(words.values_list('word', flat=True))

        for words_with_translate in words_with_translate:
            word, translates_word = words_with_translate.split(': ')
            if word not in new_words or len(word) < 3:
                continue

            type_of_word = type_word
            if ' ' in word:
                type_of_word = type_phrase

            WordsModel.objects.create(word=word, translation={'ru': translates_word}, type_word=type_of_word)

        words = WordsModel.objects.filter(Q(word__in=all_words))

        book_sentence, created = BooksSentencesModel.objects.update_or_create(
            book=instance,
            order=global_index,
            defaults={
                'text': english_sentence,
                'translation': {'ru': russian_sentence},
                'sentence_times': sentence_times,
                'description_time': description_time,
            }
        )

        book_sentence.words.set(words)

        global_index += 1
