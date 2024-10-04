from loguru import logger

from books.choices import TypeWordId
from books.dto import WordFromSentenceDTO
from books.models import WordsModel


class CreateWordsForSentenceService:
    """
    Create words for sentence.
    """

    def __init__(self, raw_words: str) -> None:
        """Init."""
        self.raw_words = raw_words
        self.words = []
        self.words_ids = []

    def work(self) -> None:
        """Start work."""
        self._create_words_objects()
        self._update_words_in_db()
        return self.words_ids

    def _create_words_objects(self) -> None:
        words_with_data = self.raw_words.split(";")
        logger.debug(f"words with data = {words_with_data}")
        for word in words_with_data:
            logger.debug(f"word = {word}")
            if not word:
                logger.debug("word is empty skip it")
                continue
            word = word.strip()
            word_data = word.split("||")
            logger.debug(f"word data = {word_data}")
            self.words.append(
                WordFromSentenceDTO(
                    word=word_data[0].strip(),
                    translate=word_data[1].strip(),
                    part_of_speech=word_data[2].strip(),
                    transcription=word_data[3].strip(),
                )
            )
        logger.debug(f"create words = {self.words}")

    def _update_words_in_db(self) -> None:
        words_from_db = WordsModel.objects.filter(word__in=[word.word for word in self.words])
        logger.debug(f"get words for database = {words_from_db}")
        for word in self.words:
            logger.debug(f"word = {word}")
            for word_from_db in words_from_db:
                condition_for_skip = {
                    word.word == word_from_db.word,
                    word.part_of_speech == word_from_db.part_of_speech,
                    word.translate in word_from_db.translation["ru"],
                }
                condition_for_update_translate = {
                    word.word == word_from_db.word,
                    word.part_of_speech == word_from_db.part_of_speech,
                }
                if all(condition_for_skip):
                    logger.debug(f"we have already this word {word_from_db.__dict__}")
                    self.words_ids.append(word_from_db.word_id)
                    break
                elif all(condition_for_update_translate):
                    logger.debug(f"we have this word but translation is different {word_from_db.__dict__}")
                    word_from_db.translation["ru"] = word_from_db.translation["ru"] + f", {word.translate}"
                    word_from_db.save(update_fields=["translation"])
                    self.words_ids.append(word_from_db.word_id)
                    break
            else:
                logger.debug("it is new word")
                type_word_id = TypeWordId.word.value
                if " " in word.word:
                    type_word_id = TypeWordId.phrase_verb.value
                new_word = WordsModel.objects.create(
                    word=word.word,
                    translation={"ru": word.translate},
                    type_word_id=type_word_id,
                    transcription=word.transcription,
                    part_of_speech=word.part_of_speech,
                )
                self.words_ids.append(new_word.word_id)
        logger.debug(f"words ids = {self.words_ids}")
