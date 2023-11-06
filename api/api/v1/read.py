from datetime import datetime
from random import choice

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload

from database import get_db
from dto.models import HistoryWordModelForReadDTO, SentenceModelForReadDTO
from dto.responses import OneResponseDTO
from functions import api_key_required
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
    prefix='/api/v1/read',
    tags=['Read'],
    dependencies=[Depends(api_key_required)],
    responses={status.HTTP_401_UNAUTHORIZED: {'description': 'Invalid API Key'}},
)


@version_1_read_router.get(
    path='/{telegram_id}/',
    response_model=OneResponseDTO[SentenceModelForReadDTO],
    responses={
        status.HTTP_404_NOT_FOUND: {'description': 'Telegram user not found.'},
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

    def __init__(self, telegram_id: int, db: Session) -> None:
        """Init."""

        self._telegram_id = telegram_id
        self._db = db
        self._is_new_sentence = True

    async def work(self) -> SentenceModelForReadDTO:
        """Start work."""
        await self._get_level_id()
        self._start_read_book = self._db.query(UsersBooksHistory).filter(
            UsersBooksHistory.telegram_user_id == self._telegram_id,
            UsersBooksHistory.end_read.is_(None),
        ).first()

        if not self._start_read_book:
            await self._get_first_sentence_from_random_book()
        else:
            self._title_book = f'{self._start_read_book.book.author} - {self._start_read_book.book.title}'
            await self._get_next_sentence()

        return await self._get_sentence_dto()

    async def _get_level_id(self):
        self._user_level_id = (
            self._db.query(Users.level_en_id)
            .filter(Users.telegram_id == self._telegram_id)
            .scalar()
        )

        if not self._user_level_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User does not have a level_en_id.')

    async def _get_first_sentence_from_random_book(self):
        """Get first sentence from random book."""
        available_books = (
            self._db.query(BooksModel)
            .options(joinedload(BooksModel.books_sentences).joinedload(BooksSentences.words))
            .filter(
                BooksModel.level_en_id == self._user_level_id
            )
            .all()
        )

        read_books = (
            self._db.query(UsersBooksHistory.book_id)
            .filter(
                UsersBooksHistory.telegram_user_id == self._telegram_id,
                UsersBooksHistory.end_read.isnot(None)
            )
            .all()
        )

        available_books = [book for book in available_books if book.book_id not in read_books]

        if available_books:
            random_book = choice(available_books)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No books available for the user.')

        self._title_book = f'{random_book.author} - {random_book.title}'

        if random_book.books_sentences:
            sorted_sentences = sorted(random_book.books_sentences, key=lambda sentence: sentence.order)
            self._need_sentence = sorted_sentences[0]
        else:
            self._need_sentence = None

        if not self._need_sentence:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No sentences available in the book.')

        new_history_book = UsersBooksHistory(telegram_user_id=self._telegram_id, book_id=self._need_sentence.book_id)
        self._db.add(new_history_book)

    async def _get_next_sentence(self):
        not_read_sentence_in_user_history = (
            self._db.query(UsersBooksSentencesHistory, BooksSentences)
            .join(BooksSentences, UsersBooksSentencesHistory.sentence_id == BooksSentences.sentence_id)
            .filter(
                UsersBooksSentencesHistory.telegram_user_id == self._telegram_id,
                UsersBooksSentencesHistory.is_read.is_(False),
                BooksSentences.book_id == self._start_read_book.book_id,
            )
            .order_by(BooksSentences.order.desc())
            .first()
        )

        if not_read_sentence_in_user_history:
            self._is_new_sentence = False
            self._need_sentence = not_read_sentence_in_user_history.BooksSentences
            self._need_sentence.history_sentence_id = not_read_sentence_in_user_history.UsersBooksSentencesHistory.id
            return

        last_read_sentence = (
            self._db.query(UsersBooksSentencesHistory, BooksSentences)
            .join(BooksSentences, UsersBooksSentencesHistory.sentence_id == BooksSentences.sentence_id)
            .filter(
                UsersBooksSentencesHistory.telegram_user_id == self._telegram_id,
                UsersBooksSentencesHistory.is_read.is_(True),
                BooksSentences.book_id == self._start_read_book.book_id,
            )
            .order_by(BooksSentences.order.desc())
            .first()
        )

        if last_read_sentence:
            last_read_order = last_read_sentence.BooksSentences.order
        else:
            last_read_order = 0

        next_sentence = (
            self._db.query(BooksSentences)
            .filter(
                BooksSentences.book_id == self._start_read_book.book_id,
                BooksSentences.order > last_read_order,
            )
            .order_by(BooksSentences.order)
            .first()
        )

        if next_sentence:
            self._need_sentence = next_sentence
            return

        self._start_read_book.end_read = datetime.utcnow()

        await self._get_first_sentence_from_random_book()

    async def _get_sentence_dto(self):

        words_with_history = (
            self._db.query(Words)
            .join(sentence_word_association, sentence_word_association.c.wordsmodel_id == Words.word_id)
            .outerjoin(
                UsersWordsHistory,
                and_(
                    UsersWordsHistory.word_id == Words.word_id,
                    UsersWordsHistory.telegram_user_id == self._telegram_id
                )
            )
            .options(joinedload(Words.users_words_history))
            .filter(sentence_word_association.c.bookssentencesmodel_id == self._need_sentence.sentence_id)
            .all()
        )

        self._need_sentence.words = words_with_history

        sentence_info = self._need_sentence.__dict__
        sentence_for_read = {}

        if sentence_info['order'] == 1:
            sentence_text = f'{self._title_book}\n\n{sentence_info["text"]}'
        else:
            sentence_text = sentence_info['text']

        sentence_for_read['sentence_id'] = sentence_info['sentence_id']
        sentence_for_read['book_id'] = sentence_info['book_id']
        sentence_for_read['text'] = sentence_text
        sentence_for_read['translation'] = sentence_info['translation']

        words_for_learn = await self._get_words_for_learn(words=sentence_info['words'])

        sentence_for_read['words'] = words_for_learn

        if self._is_new_sentence:
            new_history_sentence = UsersBooksSentencesHistory(
                telegram_user_id=self._telegram_id,
                sentence_id=sentence_info['sentence_id'],
                check_words=[word['word_id'] for word in words_for_learn],
            )
            self._db.add(new_history_sentence)
            self._db.flush()
            sentence_for_read['history_sentence_id'] = new_history_sentence.id
        else:
            sentence_for_read['history_sentence_id'] = sentence_info['history_sentence_id']
        self._db.commit()

        sentence = SentenceModelForReadDTO(**sentence_for_read)

        return sentence

    async def _get_words_for_learn(self, words: list) -> list:
        """Get words for learn."""

        check_words = []

        if self._is_new_sentence is False:
            check_words = self._need_sentence.users_books_sentences_history[0].check_words

        words_for_learn = []
        for word in words:
            word = word.__dict__
            word_info = {}
            words_history = {}
            if word['users_words_history']:
                words_history = word['users_words_history'][0].__dict__

            is_known_word = words_history.get('is_known', False)

            if check_words and word['word_id'] not in check_words:
                continue

            word_info['word_id'] = word['word_id']
            word_info['word'] = word['word']
            word_info['type_word_id'] = word['type_word_id']
            word_info['translation'] = word['translation']
            word_info['is_known'] = is_known_word
            word_info['count_view'] = words_history.get('count_view', 0)
            word_info['correct_answers'] = words_history.get('correct_answers', 0)
            word_info['incorrect_answers'] = words_history.get('incorrect_answers', 0)
            word_info['correct_answers_in_row'] = words_history.get('correct_answers_in_row', 0)

            if word_info and is_known_word is False and len(words_for_learn) < 5:
                words_for_learn.append(HistoryWordModelForReadDTO(**word_info).dict())

        return words_for_learn
