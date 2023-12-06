from re import search, sub

from nltk.tokenize import sent_tokenize
from nltk import pos_tag
import spacy

from books.choices import TypeWord
from books.dto import SentenceDTO
from books.models import WordsModel


class CreateWordsAndSentencesService:
    """ Create words and sentences service. """

    _book_text: str
    _len_sentence_by_level: dict[int, int] = {1: 30, 2: 50, 3: 70, 4: 90, 5: 120, 6: 150}

    def __init__(self):
        """Init."""
        self._idioms = WordsModel.objects.filter(
            type_word__title=TypeWord.idiomatic_expression.value).values_list('word', flat=True)

        self._phrasal_verbs = WordsModel.objects.filter(
            type_word__title=TypeWord.word.value).values_list('word', flat=True)

        self._missed_words = ('a', 'an', 'the', 'to', 'of', 'in', 'for', 'on', 'at', 'by', 'or', 'and', 'with', 'from')

        self._nlp = spacy.load('en_core_web_sm')

    def work(self, text: str, level: int) -> list[SentenceDTO]:
        """Create words and sentences.

        Args:
            text (str): text of book
            level (int): level of book
        :return: list of sentences
        """

        sentences = sent_tokenize(text)
        sentences_by_level = []

        temp_sentence = ''
        index = 0
        for index_sentence, sentence in enumerate(sentences):
            if not temp_sentence:
                temp_sentence = sentence
            elif len(temp_sentence) < self._len_sentence_by_level[level]:
                temp_sentence += f' {sentence}'
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
                )

                sentences_by_level.append(sentence_info)
                temp_sentence = sentence

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
                )

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
            token = token.strip()

            if search(r'\d', token):
                continue
            
            if token in self._missed_words or token.istitle() or len(token) < 3:
                continue

            pos = pos_tag([token])[0][1]

            if pos not in ['NNP', 'NNPS']:
                words.append(token)

        return set(words)
