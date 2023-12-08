from nltk.tokenize import sent_tokenize

from ai_app import AISDK
from books.dto import SentenceDTO


class CreateWordsAndSentencesService:
    """ Create words and sentences service. """

    _book_text: str
    _len_sentence_by_level: dict[str, int] = {
        'beginner': 30,
        'elementary': 50,
        'pre-intermediate': 70,
        'intermediate': 90,
        'upper-intermediate': 120,
        'advanced': 150,
    }

    def __init__(self):
        """Init."""
        self._sentences_by_level = []
        self._index = 0
        self._sentence = ''

    def work(self, text: str, level: str) -> list[SentenceDTO]:
        """
        Create words and sentences.

        Args:
            text (str): text of book
            level (int): level of book
        :return: list of sentences
        """

        sentences = sent_tokenize(text=text, language='english')
        for sentence in sentences:
            sentence = sentence.strip()
            if not self._sentence:
                self._sentence = sentence
            elif len(self._sentence) < self._len_sentence_by_level[level]:
                self._sentence += f' {sentence}'
            else:
                self._index += 1
                self._create_sentence_info(level=level)

        if self._sentence:
            self._create_sentence_info(level=level)

        return self._sentences_by_level

    def _create_sentence_info(self, level: str) -> None:
        all_words = AISDK().get_words(sentence=self._sentence, english_level=level)
        idioms = []
        phrasal_verbs = []
        words = []

        for word in all_words:
            count_words_in_word = len(word.split(' '))
            if count_words_in_word > 3:
                idioms.append(word)
            elif count_words_in_word > 1:
                phrasal_verbs.append(word)
            else:
                words.append(word)

        sentence_info = SentenceDTO(
            text=self._sentence,
            index=self._index,
            idiomatic_expression=idioms,
            phrase_verb=phrasal_verbs,
            words=words,
        )

        self._sentences_by_level.append(sentence_info)
