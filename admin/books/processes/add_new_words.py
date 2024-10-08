from books.models import TypeWordsModel, WordsModel


class AddNewWordsProcess:
    """Add new words to the database."""

    def __call__(self, words: list[dict[str, str]], type_words: str) -> None:
        """
        Call this function to add new words to the database.

        :param words: List of dictionaries with words.
        :param type_words: Type of words.
        """
        self._type_words = TypeWordsModel.objects.get(title=type_words)

        self._words = words
        self._add_words_to_database()

    def _add_words_to_database(self) -> None:
        for word in self._words:
            WordsModel.objects.update_or_create(
                word=word["word"],
                defaults={
                    "type_word": self._type_words,
                    "translation": word["translate"],
                },
            )
