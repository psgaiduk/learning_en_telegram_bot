import os
import sys

# Используйте абсолютный путь к корневому каталогу вашего проекта
project_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root_path)

from json import load

from re import sub
from loguru import logger
from nltk.tokenize import sent_tokenize
from nltk import pos_tag
import spacy


class AddNewBookToDB:

    def __init__(self):
        """Init."""
        with open('idioms.json', 'r') as idioms:
            self._idioms = set(load(idioms).keys())

        with open('phrases_verbs.json', 'r') as phrasal_verbs:
            self._phrasal_verbs = set(load(phrasal_verbs).keys())

        self._missed_words = ('a', 'an', 'the', 'to', 'of', 'in', 'for', 'on', 'at', 'by', 'or', 'and', 'with', 'from')

        self._nlp = spacy.load('en_core_web_sm')

    def work(self):
        self._open_book()
        self._create_text_for_insert()

    def _open_book(self):
        with open('new_book.txt', 'r') as book_text:
            self._book_text = book_text.read()

    def _create_text_for_insert(self):

        self._create_sentences_by_level()

        self._text_for_insert = []

        for sentence in self._sentences_by_level:
            self._sentence = sentence

            idioms = self._create_idioms()
            phrasal_verbs = self._create_phrasal_verbs()

            clean_sentence = sub(r'[^\w\s]', '', self._sentence)
            doc = self._nlp(clean_sentence)

            self._lemmatized_tokens = [token.lemma_ for token in doc if not token.is_punct]

            words = self._create_words()

            self._text_for_insert.append({
                'sentence': sentence,
                'idioms': idioms,
                'phrasal_verbs': phrasal_verbs,
                'words': words,
            })

    def _create_sentences_by_level(self) -> None:
        sentences = sent_tokenize(self._book_text)
        self._sentences_by_level = []

        temp_sentence = ''
        for sentence in sentences:
            if len(temp_sentence) < 100:
                temp_sentence += f' {sentence}'
            else:
                self._sentences_by_level.append(temp_sentence)
                temp_sentence = sentence

        if temp_sentence:
            self._sentences_by_level.append(temp_sentence)

    def _create_idioms(self) -> set[str]:
        idioms = []
        for idiom in self._idioms:
            if idiom in self._sentence:
                self._sentence.replace(idiom, '')
                idioms.append(idiom)

        return set(idioms)

    def _create_phrasal_verbs(self) -> set[str]:
        phrasal_verbs = []
        for phrasal_verb in self._phrasal_verbs:
            if phrasal_verb in self._sentence:
                self._sentence.replace(phrasal_verb, '')
                phrasal_verbs.append(phrasal_verb)

        return set(phrasal_verbs)

    def _create_words(self) -> set[str]:
        words = []
        for token in self._lemmatized_tokens:
            if token in self._missed_words or token.istitle():
                continue

            pos = pos_tag([token])[0][1]

            if pos not in ['NNP', 'NNPS']:
                words.append(token)

        return set(words)


if __name__ == "__main__":
    logger.configure(extra={'chat_id': 1, 'work_id': 1})
    AddNewBookToDB().work()
