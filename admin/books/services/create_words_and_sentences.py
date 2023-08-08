from re import sub

from nltk.tokenize import sent_tokenize
from nltk import pos_tag
import spacy

from books.choices import TypeWord
from books.dto import SentenceDTO
from books.models import WordsModel
from telegram_users.choices import Language
from nlp_translate import translate_text


class CreateWordsAndSentencesService:
    """ Create words and sentences service. """

    _book_text: str

    def __init__(self):
        """Init."""
        self._idioms = WordsModel.objects.filter(
            type_word__title=TypeWord.idiomatic_expression.value).values_list('word', flat=True)

        self._phrasal_verbs = WordsModel.objects.filter(
            type_word__title=TypeWord.word.value).values_list('word', flat=True)

        self._missed_words = ('a', 'an', 'the', 'to', 'of', 'in', 'for', 'on', 'at', 'by', 'or', 'and', 'with', 'from')

        self._nlp = spacy.load('en_core_web_sm')

    def work(self, text: str) -> list[SentenceDTO]:

        sentences = sent_tokenize(text)
        translate_sentences = self._translate_text(text=text)
        sentences_by_level = []

        temp_sentence = ''
        translates_sentence = {language_code: '' for language_code, _ in Language.choices()}
        index = 0
        for index_sentence, sentence in enumerate(sentences):
            if not temp_sentence:
                temp_sentence = sentence
                for language_code, _ in Language.choices():
                    translates_sentence[language_code] = translate_sentences[language_code][index_sentence]
            elif len(temp_sentence) < 100:
                temp_sentence += f' {sentence}'
                for language_code, _ in Language.choices():
                    translates_sentence[language_code] += f' {translate_sentences[language_code][index_sentence]}'
            else:
                index += 1
                update_sentence, idioms = self._create_idioms(temp_sentence)
                update_sentence, phrasal_verbs = self._create_phrasal_verbs(update_sentence)
                words = self._create_words(update_sentence)

                sentence_info = SentenceDTO(
                    text=temp_sentence,
                    index=index,
                    idiomatic_expression=idioms,
                    phrase_verb=phrasal_verbs,
                    words=words,
                    translate=translates_sentence,
                )

                sentences_by_level.append(sentence_info)
                temp_sentence = sentence
                for language_code, _ in Language.choices():
                    translates_sentence[language_code] = translate_sentences[language_code][index_sentence]

        if temp_sentence:
            sentence, idioms = self._create_idioms(temp_sentence)
            sentence, phrasal_verbs = self._create_phrasal_verbs(sentence)
            words = self._create_words(sentence)

            sentence_info = SentenceDTO(
                text=temp_sentence,
                index=index,
                idiomatic_expression=idioms,
                phrase_verb=phrasal_verbs,
                words=words,
                translate=translates_sentence,
                )

            for language_code, _ in Language.choices():
                translates_sentence[language_code] = translate_sentences[language_code][index_sentence]

            sentences_by_level.append(sentence_info)

        return sentences_by_level

    def _create_idioms(self, sentence: str) -> tuple[str, set[str]]:
        temp_sentence = sentence
        idioms = []
        for idiom in self._idioms:
            if idiom in temp_sentence:
                temp_sentence.replace(idiom, '')
                idioms.append(idiom)

        return temp_sentence, set(idioms)

    def _create_phrasal_verbs(self, sentence: str) -> tuple[str, set[str]]:
        phrasal_verbs = []
        for phrasal_verb in self._phrasal_verbs:
            if phrasal_verb in sentence:
                sentence.replace(phrasal_verb, '')
                phrasal_verbs.append(phrasal_verb)

        return sentence, set(phrasal_verbs)

    def _create_words(self, sentence: str) -> set[str]:
        words = []
        clean_sentence = sub(r'[^\w\s]', '', sentence)
        doc = self._nlp(clean_sentence)

        tokens = [token.lemma_ for token in doc if not token.is_punct]
        for token in tokens:
            if token in self._missed_words or token.istitle() or len(token) < 3:
                continue

            pos = pos_tag([token])[0][1]

            if pos not in ['NNP', 'NNPS']:
                words.append(token)

        return set(words)

    def _translate_text(self, text: str) -> dict[str, list[str]]:
        BATCH_SIZE: int = 3000
        translates_sentence = {}
        sentences = sent_tokenize(text)

        for language_code, language_name in Language.get_info():
            if not translates_sentence.get(language_code):
                translates_sentence[language_code] = ''

            current_batch = ''
            for sentence in sentences:
                if len(current_batch) + len(sentence) <= BATCH_SIZE:
                    current_batch += sentence
                else:
                    translated_batch = translate_text(text_on_en=current_batch, language=language_code)
                    translates_sentence[language_code] += translated_batch
                    current_batch = sentence

            if current_batch:
                translated_batch = translate_text(text_on_en=current_batch, language=language_code)
                translates_sentence[language_code] += translated_batch

            translates_sentence[language_code] = sent_tokenize(
                translates_sentence[language_code],
                language=language_name,
            )

        return translates_sentence
