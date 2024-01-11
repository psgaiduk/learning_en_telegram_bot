from math import ceil

from django.db.models import Q
from django_q.tasks import Chain
from loguru import logger
from nltk import sent_tokenize

from ai_app import AISDK
from books.models import BooksModel, BooksSentencesModel, WordsModel
from nlp_translate import translate_text


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
    count_parts = ceil(len(instance.text) / 700)
    avg_length = len(instance.text) / count_parts
    logger.debug(f'Count parts {count_parts}, avg length {avg_length}')
    chunk = ""
    for sentence in sentences:
        if len(chunk) + len(sentence) <= avg_length:
            chunk += " " + sentence
        else:
            chunk += " " + sentence
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
    for sentence in sentences:
        sentence_data = sentence.split('---')
        english_sentence = sentence_data[0].strip()
        logger.debug(f'English sentence {english_sentence}')
        russian_sentence = sentence_data[1].strip()
        logger.debug(f'Russian sentence {russian_sentence}')
        words_with_type = sentence_data[2].replace('.', '').split('; ')
        logger.debug(f'Words with type {words_with_type}')
        sentence_times = sentence_data[3].strip()
        logger.debug(f'Sentence times {sentence_times}')
        description_time = sentence_data[4].strip()
        logger.debug(f'Description time {description_time}')

        AISDK().create_audio_file(sentence=english_sentence, file_name=f'{instance.book_id} - {global_index}')

        words = [
            {'word': word.split(' - ')[0].strip().lower(), 'word_type': word.split(' - ')[1].strip()}
            for word in words_with_type if ' - ' in word
        ]
        logger.debug(f'Words {words}')
        english_words = [word['word'] for word in words]
        logger.debug(f'English words {english_words}')
        words_in_database = WordsModel.objects.filter(word__in=english_words)
        logger.debug(f'Words in database {words_in_database}')
        new_english_words = set(english_words) - set(words_in_database.values_list('word', flat=True))
        logger.debug(f'Words for translate {new_english_words}')
        if new_english_words:
            words_for_translate = '; '.join(english_words)
            translate_words = translate_text(text_on_en=words_for_translate, language='ru').split('; ')
            logger.debug(f'Translates words {translate_words}')

            for index_word, word in enumerate(words):
                if word['word'] not in new_english_words:
                    continue
                english_word = word['word']
                type_word = int(word['word_type'])
                translate_word = translate_words[index_word].lower()
                logger.debug(f'English word {english_word} - {type_word} - {translate_word}')
                WordsModel.objects.create(word=english_word, translation={'ru': translate_word}, type_word_id=type_word)

        words = WordsModel.objects.filter(Q(word__in=english_words))

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
