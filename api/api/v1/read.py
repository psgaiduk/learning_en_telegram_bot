from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy import Boolean, and_, func, select
from sqlalchemy.orm import Session, contains_eager, joinedload, subqueryload

from database import get_db
from dto.models import HistoryWordModelForReadDTO, SentenceModelForReadDTO
from dto.responses import OneResponseDTO
from functions import api_key_required, replace_with_translation
from models import (
    BooksModel,
    BooksSentences,
    Users,
    UsersBooksHistory,
    UsersBooksSentencesHistory,
    UsersWordsHistory,
    Words,
    sentence_word_association,
)


version_1_read_router = APIRouter(
    prefix="/api/v1/read",
    tags=["Read"],
    dependencies=[Depends(api_key_required)],
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "Invalid API Key"}},
)


@version_1_read_router.get(
    path="/{telegram_id}/",
    response_model=OneResponseDTO[SentenceModelForReadDTO],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Telegram user not found."},
        status.HTTP_206_PARTIAL_CONTENT: {"description": "You have  read the maximum number of sentences today."},
    },
    status_code=status.HTTP_200_OK,
)
async def read_book_for_user(telegram_id: int, db: Session = Depends(get_db)):
    """Read book for user."""

    read_book_service = ReadBookService(telegram_id, db)
    sentence = await read_book_service.work()

    return OneResponseDTO(detail=sentence)


class ReadBookService:
    """Read book service."""

    _telegram_id: int
    _db: Session
    _is_new_sentence: bool
    _user: Users

    def __init__(self, telegram_id: int, db: Session) -> None:
        """Init."""

        self._telegram_id = telegram_id
        self._db = db
        self._is_new_sentence = True
        self._title_book = ""

    async def work(self) -> SentenceModelForReadDTO:
        """Start work."""
        await self._get_user()
        await self._check_count_read_sentences_today()

        need_sentence = (
            self._db.query(BooksSentences)
            .join(UsersBooksHistory, BooksSentences.book_id == UsersBooksHistory.book_id)
            .outerjoin(
                UsersBooksSentencesHistory,
                and_(
                    BooksSentences.sentence_id == UsersBooksSentencesHistory.sentence_id,
                    UsersBooksSentencesHistory.created_at >= UsersBooksHistory.start_read,
                ),
            )
            .filter(UsersBooksHistory.telegram_user_id == self._telegram_id)
            .filter(UsersBooksHistory.end_read == None)
            .filter(UsersBooksSentencesHistory.created_at == None)
            .order_by(BooksSentences.order)
            .options(subqueryload(BooksSentences.tenses))
        )
        logger.debug(f"query get sentence for started book = {need_sentence}")
        self._need_sentence = need_sentence.first()
        logger.debug(f"need sentence from started book = {self._need_sentence}")

        if not self._need_sentence:
            subquery1 = (
                self._db.query(
                    BooksModel.book_id.label("book_id"),
                    BooksModel.title.label("title"),
                    BooksModel.author.label("author"),
                    func.cast(False, Boolean).label("repeat"),
                )
                .outerjoin(
                    UsersBooksHistory,
                    (UsersBooksHistory.book_id == BooksModel.book_id)
                    & (UsersBooksHistory.telegram_user_id == self._telegram_id),
                )
                .filter(UsersBooksHistory.start_read.is_(None))
                .limit(1)
            )

            subquery2 = (
                self._db.query(
                    BooksModel.book_id.label("book_id"),
                    BooksModel.title.label("title"),
                    BooksModel.author.label("author"),
                    func.cast(True, Boolean).label("repeat"),
                )
                .order_by(func.random())
                .limit(1)
            )

            union_subquery = subquery1.union_all(subquery2).limit(1).subquery()

            need_sentence = (
                self._db.query(BooksSentences)
                .join(union_subquery, BooksSentences.book_id == union_subquery.c.book_id)
                .filter(BooksSentences.order == 1)
                .options(subqueryload(BooksSentences.tenses))
                .add_columns(union_subquery.c.title, union_subquery.c.author, union_subquery.c.repeat)
            )

            logger.debug(f"query get sentence = {need_sentence}")
            need_sentence = need_sentence.first()
            logger.debug(f"get started book = {need_sentence}")

            self._title_book = f"{need_sentence.author} - {need_sentence.title}"

            if need_sentence.repeat:
                self._title_book = (
                    "Закончились доступные книги на этом уровне. "
                    f"Повторим ранее прочитанную книгу\n{self._title_book}\n"
                )

            self._need_sentence = need_sentence[0]
            logger.debug(f"get started book = {self._need_sentence}")

            new_history_book = UsersBooksHistory(
                telegram_user_id=self._telegram_id,
                book_id=self._need_sentence.book_id,
            )
            self._db.add(new_history_book)

        return await self._get_sentence_dto()

    async def _get_user(self):
        self._user = (
            self._db.query(Users)
            .filter(Users.telegram_id == self._telegram_id)
            .options(joinedload(Users.hero_level))
            .first()
        )
        logger.debug(f"Get users by id {self._telegram_id}")
        logger.debug(f"User: {self._user}")

        if not self._user:
            logger.debug(f"User not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    async def _check_count_read_sentences_today(self):
        logger.debug(f"Check count read sentences")
        count_read_sentences = (
            self._db.query(func.count(UsersBooksSentencesHistory.sentence_id))
            .filter(
                UsersBooksSentencesHistory.telegram_user_id == self._telegram_id,
                func.date(UsersBooksSentencesHistory.created_at) == func.date(func.now()),
                UsersBooksSentencesHistory.is_read.is_(True),
            )
            .scalar()
        )

        logger.debug(f"Count read sentences: {count_read_sentences}")

        if count_read_sentences >= self._user.hero_level.count_sentences:
            raise HTTPException(
                status_code=status.HTTP_206_PARTIAL_CONTENT,
                detail="You have  read the maximum number of sentences today.",
            )

    async def _get_sentence_dto(self):
        subquery = select(sentence_word_association.c.wordsmodel_id).where(
            sentence_word_association.c.bookssentencesmodel_id == self._need_sentence.sentence_id
        )

        words_with_history = (
            self._db.query(Words)
            .outerjoin(UsersWordsHistory, UsersWordsHistory.telegram_user_id == self._telegram_id)
            .filter(Words.word_id.in_(subquery))
            .options(contains_eager(Words.users_words_history))
        )

        logger.debug(f"query = {str(words_with_history)}")
        words_with_history = words_with_history.all()

        sentence_for_read = {}
        sentence_text = self._need_sentence.text
        sentence_for_read["words"] = words_with_history
        sentence_for_read["sentence_id"] = self._need_sentence.sentence_id
        sentence_for_read["book_id"] = self._need_sentence.book_id
        sentence_for_read["translation"] = self._need_sentence.translation
        sentence_for_read["order"] = self._need_sentence.order
        sentence_for_read["sentence_times"] = []
        sentence_for_read["description_time"] = []

        for tense in self._need_sentence.tenses:
            logger.debug(f"tense: {tense.__dict__}")
            sentence_for_read["sentence_times"].append(tense.name)
            sentence_for_read["description_time"].append(tense.short_description)

        sentence_for_read["sentence_times"] = ", ".join(sentence_for_read["sentence_times"])
        sentence_for_read["description_time"] = "\n".join(sentence_for_read["description_time"])

        words_for_learn, words_for_sentence = await self._get_words_for_learn(words=sentence_for_read["words"])

        text_with_words = replace_with_translation(text=sentence_text, words=words_for_sentence["all"])
        text_with_new_words = replace_with_translation(text=sentence_text, words=words_for_sentence["new"])
        logger.debug(f"text with words = {text_with_words}")
        logger.debug(f"text with new words = {text_with_new_words}")

        if self._need_sentence.order == 1:
            logger.debug(f"it is first sentence in book add title")
            sentence_text = f"{self._title_book}\n\n{sentence_text}"
        else:
            sentence_text = sentence_text
        logger.debug(f"sentence text = {sentence_text}")
        sentence_for_read["text"] = sentence_text

        sentence_for_read["text_with_words"] = text_with_words
        sentence_for_read["text_with_new_words"] = text_with_new_words
        sentence_for_read["words"] = words_for_learn

        if self._is_new_sentence:
            logger.debug("it is new sentence save history in db")
            new_history_sentence = UsersBooksSentencesHistory(
                telegram_user_id=self._telegram_id,
                sentence_id=self._need_sentence.sentence_id,
                check_words=[word["word_id"] for word in words_for_learn],
            )
            self._db.add(new_history_sentence)
            self._db.flush()
            sentence_for_read["history_sentence_id"] = new_history_sentence.id
        else:
            sentence_for_read["history_sentence_id"] = self._need_sentence.history_sentence_id
        self._db.commit()

        sentence = SentenceModelForReadDTO(**sentence_for_read)
        logger.debug(f"create sentence = {sentence}")

        return sentence

    async def _get_words_for_learn(self, words: list) -> tuple[list, dict]:
        """Get words for learn."""
        logger.debug("start add words for learn")
        check_words = []

        if self._is_new_sentence is False:
            logger.debug("it is old sentence")
            check_words = self._need_sentence.check_words or [0]
        logger.debug(f"check words = {check_words}")

        words_for_learn = []
        words_for_sentence = {"all": [], "new": []}
        for word in words:
            logger.debug(f"add word {word}")
            word_info = {}
            words_history = {}
            if word.users_words_history:
                words_history = word.users_words_history[0].__dict__
                logger.debug(f"word has history = {words_history}")
            is_known_word = words_history.get("is_known", False)

            words_for_sentence["all"].append(word)
            if is_known_word is False:
                logger.debug("user does not know this word add word")
                words_for_sentence["new"].append(word)

            if check_words and word.word_id not in check_words:
                logger.debug("this word not in check_words skip it")
                continue

            word_info["telegram_user_id"] = self._telegram_id
            word_info["word_id"] = word.word_id
            word_info["word"] = word.word
            word_info["transcription"] = word.transcription
            word_info["type_word_id"] = word.type_word_id
            word_info["translation"] = word.translation
            word_info["is_known"] = is_known_word
            word_info["count_view"] = words_history.get("count_view", 0)
            word_info["correct_answers"] = words_history.get("correct_answers", 0)
            word_info["incorrect_answers"] = words_history.get("incorrect_answers", 0)
            word_info["correct_answers_in_row"] = words_history.get("correct_answers_in_row", 0)
            word_info["increase_factor"] = words_history.get("increase_factor", 0)
            word_info["interval_repeat"] = words_history.get("interval_repeat", 0)
            word_info["repeat_datetime"] = words_history.get("repeat_datetime", datetime.now())

            if word_info and is_known_word is False:
                logger.debug("user does not know this word add to words for learn")
                words_for_learn.append(HistoryWordModelForReadDTO(**word_info).dict())

                if not words_history:
                    logger.debug("user does not have history for this word add it in db")
                    new_word = UsersWordsHistory(
                        telegram_user_id=word_info["telegram_user_id"],
                        word_id=word_info["word_id"],
                        is_known=word_info["is_known"],
                        count_view=word_info["count_view"],
                        correct_answers=word_info["correct_answers"],
                        incorrect_answers=word_info["incorrect_answers"],
                        correct_answers_in_row=word_info["correct_answers_in_row"],
                        repeat_datetime=datetime.utcnow(),
                    )
                    self._db.add(new_word)
            if is_known_word is True:
                continue
        logger.debug(f"words for learn = {words_for_learn}")
        logger.debug(f"words for sentence = {words_for_sentence}")
        return words_for_learn, words_for_sentence
