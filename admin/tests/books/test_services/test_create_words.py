from pytest import fixture, mark

from django.db.models import Q

from books.dto import WordFromSentenceDTO
from books.models import WordsModel
from books.services import CreateWordsForSentenceService
from tests.fixtures import *


class TestCreateWordsForSentenceService:
    """Tests for CheckWordsService."""

    @fixture(autouse=True)
    def setup_method(self, words_from_text):
        self.raw_words = words_from_text
        self.service = CreateWordsForSentenceService(raw_words=self.raw_words)

    def test_create_words_objects(self):
        self.service._create_words_objects()
        words_dto = []
        words_with_data = self.raw_words.split(";")
        for word in words_with_data:
            if not word:
                continue
            word = word.strip()
            word_data = word.split("||")
            words_dto.append(
                WordFromSentenceDTO(
                    word=word_data[0].strip(),
                    translate=word_data[1].strip(),
                    part_of_speech=word_data[2].strip(),
                    transcription=word_data[3].strip(),
                )
            )

        assert self.service.words == words_dto

    @mark.django_db
    def test_get_words_for_all_create(self):
        word = WordFromSentenceDTO(word="word", translate="слово", part_of_speech="n", transcription="word")
        word_1 = WordFromSentenceDTO(word="word", translate="словить", part_of_speech="v", transcription="word")
        word_2 = WordFromSentenceDTO(word="work", translate="работа", part_of_speech="v", transcription="work")
        words_in_db = WordsModel.objects.all()
        assert len(words_in_db) == 0
        self.service.words = [word, word_1, word_2]
        self.service._update_words_in_db()
        words_in_db = WordsModel.objects.all()
        assert len(words_in_db) == 3
        word_2_from_db = WordsModel.objects.filter(word=word_2.word).first()
        assert word_2_from_db.word == word_2.word
        assert word_2_from_db.part_of_speech == word_2.part_of_speech
        assert word_2.transcription == word_2.transcription
        assert set(self.service.words_ids) == {word.word_id for word in words_in_db}

    @mark.django_db
    def test_get_words_for_all_create_with_same_word_another_part_of_speech(self):
        word = WordFromSentenceDTO(word="word", translate="слово", part_of_speech="n", transcription="word")
        word_1 = WordFromSentenceDTO(word="word", translate="словить", part_of_speech="v", transcription="word")
        word_2 = WordFromSentenceDTO(word="work", translate="работа", part_of_speech="v", transcription="work")
        self.service.words = [word_1, word_2]
        WordsModel.objects.create(
            word=word.word,
            translation={"ru": word.translate},
            type_word_id=1,
            transcription=word.transcription,
            part_of_speech=word.part_of_speech,
        )
        words_in_db = WordsModel.objects.all()
        assert len(words_in_db) == 1
        self.service._update_words_in_db()
        words_in_db = WordsModel.objects.all()
        assert len(words_in_db) == 3
        new_words = words_in_db.filter(
            Q(word=word_1.word, part_of_speech=word_1.part_of_speech)
            | Q(word=word_2.word, part_of_speech=word_2.part_of_speech)
        )
        assert set(self.service.words_ids) == {word.word_id for word in new_words}

    @mark.django_db
    def test_get_words_for_all_update_same_word_with_new_translate(self):
        word = WordFromSentenceDTO(word="word", translate="слово", part_of_speech="n", transcription="word")
        word_1 = WordFromSentenceDTO(word="word", translate="словить", part_of_speech="n", transcription="word")
        word_2 = WordFromSentenceDTO(word="work", translate="работа", part_of_speech="v", transcription="work")
        self.service.words = [word_1]
        WordsModel.objects.create(
            word=word.word,
            translation={"ru": word.translate},
            type_word_id=1,
            transcription=word.transcription,
            part_of_speech=word.part_of_speech,
        )
        WordsModel.objects.create(
            word=word_2.word,
            translation={"ru": word_2.translate},
            type_word_id=1,
            transcription=word_2.transcription,
            part_of_speech=word_2.part_of_speech,
        )
        words_in_db = WordsModel.objects.all()
        assert len(words_in_db) == 2
        self.service._update_words_in_db()
        words_in_db = WordsModel.objects.all()
        assert len(words_in_db) == 2
        assert words_in_db.filter(word=word.word).first().translation["ru"] == "слово, словить"
        new_words = words_in_db.filter(Q(word=word_1.word, part_of_speech=word_1.part_of_speech))
        assert set(self.service.words_ids) == {word.word_id for word in new_words}

    @mark.django_db
    def test_get_words_for_same_word(self):
        word = WordFromSentenceDTO(word="word", translate="слово", part_of_speech="n", transcription="word")
        word_1 = WordFromSentenceDTO(word="word", translate="слово", part_of_speech="n", transcription="word")
        self.service.words = [word_1]
        WordsModel.objects.create(
            word=word.word,
            translation={"ru": word.translate},
            type_word_id=1,
            transcription=word.transcription,
            part_of_speech=word.part_of_speech,
        )
        words_in_db = WordsModel.objects.all()
        assert len(words_in_db) == 1
        self.service._update_words_in_db()
        words_in_db = WordsModel.objects.all()
        assert len(words_in_db) == 1
        assert words_in_db.first().translation["ru"] == "слово"
        new_words = words_in_db.filter(Q(word=word_1.word, part_of_speech=word_1.part_of_speech))
        assert set(self.service.words_ids) == {word.word_id for word in new_words}
        # Контрольная проверка, что добавляется новое слово
        word_2 = WordFromSentenceDTO(word="work", translate="работа", part_of_speech="v", transcription="work")
        self.service.words = [word_2]
        self.service.words_ids = []
        self.service._update_words_in_db()
        words_in_db = WordsModel.objects.all()
        assert len(words_in_db) == 2
        new_words = words_in_db.filter(word=word_2.word, part_of_speech=word_2.part_of_speech)
        assert set(self.service.words_ids) == {word.word_id for word in new_words}

    @mark.django_db
    def test_get_words_for_same_word_with_many_translates(self):
        word = WordFromSentenceDTO(word="word", translate="слово, словечко", part_of_speech="n", transcription="word")
        word_1 = WordFromSentenceDTO(word="word", translate="слово", part_of_speech="n", transcription="word")
        self.service.words = [word_1]
        WordsModel.objects.create(
            word=word.word,
            translation={"ru": word.translate},
            type_word_id=1,
            transcription=word.transcription,
            part_of_speech=word.part_of_speech,
        )
        words_in_db = WordsModel.objects.all()
        assert len(words_in_db) == 1
        self.service._update_words_in_db()
        words_in_db = WordsModel.objects.all()
        assert len(words_in_db) == 1
        assert words_in_db.first().translation["ru"] == "слово, словечко"
        new_words = words_in_db.filter(Q(word=word_1.word, part_of_speech=word_1.part_of_speech))
        assert set(self.service.words_ids) == {word.word_id for word in new_words}
