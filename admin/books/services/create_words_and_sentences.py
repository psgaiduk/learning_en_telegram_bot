from nltk.tokenize import sent_tokenize

from ai_app import AISDK
from books.dto import SentenceDTO


class CreateWordsAndSentencesService:
    """ Create words and sentences service. """

    _book_text: str
    _len_sentence_by_level: dict[str, int] = {'A1': 30, 'A2': 50, 'B1': 70, 'B2': 90, 'C1': 120, 'C2': 150}

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
                self._create_sentence_info(level=level)
                self._sentence = sentence

        if self._sentence:
            self._create_sentence_info(level=level)

        return self._sentences_by_level

    def _create_sentence_info(self, level: str) -> None:
        self._index += 1
        all_words = AISDK().get_words(sentence=self._sentence, english_level=level)
        words = {1: [], 2: [], 3: []}

        for word in all_words:
            if '- 1' in word:
                words[3].append(word.replace(' - 1', '').strip())
            elif '- 2' in word:
                words[2].append(word.replace(' - 2', '').strip())
            elif '- 3' in word:
                words[1].append(word.replace(' - 3', '').strip())

        sentence_info = SentenceDTO(
            text=self._sentence,
            index=self._index,
            words=words,
        )

        self._sentences_by_level.append(sentence_info)
