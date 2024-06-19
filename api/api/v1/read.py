from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy import and_, func, not_
from sqlalchemy.orm import Session, aliased, joinedload

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
        status.HTTP_206_PARTIAL_CONTENT: {'description': 'You have  read the maximum number of sentences today.'},
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

    async def work(self) -> SentenceModelForReadDTO:
        """Start work."""
        await self._get_user()
        await self._check_count_read_sentences_today()

        self._start_read_book = self._db.query(UsersBooksHistory).filter(
            UsersBooksHistory.telegram_user_id == self._telegram_id,
            UsersBooksHistory.end_read.is_(None),
        ).first()

        if not self._start_read_book:
            await self._get_first_sentence_from_book()
        else:
            self._title_book = f'{self._start_read_book.book.author} - {self._start_read_book.book.title}'
            await self._get_next_sentence()

        return await self._get_sentence_dto()

    async def _get_user(self):
        self._user = (
            self._db.query(Users)
            .filter(Users.telegram_id == self._telegram_id)
            .options(joinedload(Users.hero_level))
            .first()
        )
        logger.debug(f'Get users by id {self._telegram_id}')
        logger.debug(f'User: {self._user}')

        if not self._user:
            logger.debug(f'User not found')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

    async def _check_count_read_sentences_today(self):
        logger.debug(f'Check count read sentences')
        count_read_sentences = (
            self._db.query(func.count(UsersBooksSentencesHistory.sentence_id))
            .filter(
                UsersBooksSentencesHistory.telegram_user_id == self._telegram_id,
                func.date(UsersBooksSentencesHistory.created_at) == func.date(func.now()),
                UsersBooksSentencesHistory.is_read.is_(True),
            )
            .scalar()
        )

        logger.debug(f'Count read sentences: {count_read_sentences}')

        if count_read_sentences >= self._user.hero_level.count_sentences:
            raise HTTPException(
                status_code=status.HTTP_206_PARTIAL_CONTENT,
                detail='You have  read the maximum number of sentences today.')

    async def _get_first_sentence_from_book(self):
        """Get first sentence from book."""
        logger.debug(f'Get first sentence from book for user {self._telegram_id}')

        next_book = await self._get_sentence_from_next_book()

        self._title_book = ''

        if next_book:
            selected_book = next_book
        else:
            selected_book = await self._get_sentence_from_random_book()
            if not selected_book:
                selected_book = await self._get_sentence_from_old_book()

        self._title_book += f'{selected_book.author} - {selected_book.title}'
        logger.debug(f'title book: {self._title_book}')

        if selected_book.books_sentences:
            sorted_sentences = sorted(selected_book.books_sentences, key=lambda sentence: sentence.order)
            self._need_sentence = sorted_sentences[0]
        else:
            self._need_sentence = None

        if not self._need_sentence:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No sentences available in the book.')

        new_history_book = UsersBooksHistory(telegram_user_id=self._telegram_id, book_id=self._need_sentence.book_id)
        self._db.add(new_history_book)

    async  def _get_sentence_from_next_book(self):
        UsersBooksHistoryAlias = aliased(UsersBooksHistory)

        last_read_book_subquery = (
            self._db.query(UsersBooksHistoryAlias.book_id)
            .filter(
                UsersBooksHistoryAlias.telegram_user_id == self._telegram_id,
                UsersBooksHistoryAlias.end_read.isnot(None)
            )
            .order_by(UsersBooksHistoryAlias.end_read.desc())
            .limit(1)
            .subquery()
        )

        next_book = (
            self._db.query(BooksModel)
            .options(
                joinedload(BooksModel.books_sentences).joinedload(BooksSentences.words),
                joinedload(BooksModel.books_sentences).joinedload(BooksSentences.tenses)
            )
            .filter(BooksModel.previous_book_id == last_read_book_subquery)
            .first()
        )

        logger.debug('Get first sentence from next book:')
        logger.debug(f'{self._telegram_id} - {next_book.__dict__ if next_book else "not found"}')

        return next_book

    async def _get_sentence_from_random_book(self):
        logger.debug(f'Get first sentence from random book for user {self._telegram_id}')

        read_books_subquery = (
            self._db.query(UsersBooksHistory.book_id)
            .filter(
                UsersBooksHistory.telegram_user_id == self._telegram_id,
                UsersBooksHistory.end_read.isnot(None)
            )
            .subquery()
        )

        selected_book = (
            self._db.query(BooksModel)
            .options(
                joinedload(BooksModel.books_sentences).joinedload(BooksSentences.words),
                joinedload(BooksModel.books_sentences).joinedload(BooksSentences.tenses)
            )
            .filter(
                BooksModel.level_en_id == self._user.level_en_id,
                not_(BooksModel.book_id.in_(read_books_subquery)),
                BooksModel.previous_book_id.is_(None),
            )
            .order_by(func.random())
            .first()
        )

        logger.debug(f'Get first sentence from random book {selected_book.__dict__ if selected_book else "not found"}')

        return selected_book

    async def _get_sentence_from_old_book(self):
        selected_book = (
            self._db.query(BooksModel)
            .options(
                joinedload(BooksModel.books_sentences).joinedload(BooksSentences.words),
                joinedload(BooksModel.books_sentences).joinedload(BooksSentences.tenses)
            )
            .filter(
                BooksModel.level_en_id == self._user.level_en_id,
                BooksModel.previous_book_id.is_(None),
            )
            .order_by(func.random())
            .first()
        )

        logger.debug(f'Get old random book {selected_book.__dict__}')

        self._title_book += f'Закончились доступные книги на этом уровне. Повторим ранее прочитанную книгу\n'

        logger.debug(f'title book: {self._title_book}')
        return selected_book

    async def _get_next_sentence(self):
        UsersBooksSentencesHistoryAlias = aliased(UsersBooksSentencesHistory)

        not_read_sentence_in_user_history = (
            self._db.query(BooksSentences, UsersBooksSentencesHistoryAlias)
            .join(
                UsersBooksSentencesHistoryAlias,
                BooksSentences.sentence_id == UsersBooksSentencesHistoryAlias.sentence_id
            )
            .filter(
                UsersBooksSentencesHistoryAlias.telegram_user_id == self._telegram_id,
                UsersBooksSentencesHistoryAlias.is_read.is_(False),
                BooksSentences.book_id == self._start_read_book.book_id,
            )
            .order_by(BooksSentences.order.desc())
            .first()
        )

        if not_read_sentence_in_user_history:
            self._is_new_sentence = False
            self._need_sentence, user_sentence_history = not_read_sentence_in_user_history
            self._need_sentence.history_sentence_id = user_sentence_history.id
            check_words = user_sentence_history.check_words
            self._need_sentence.check_words = check_words
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

        await self._get_first_sentence_from_book()

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
        logger.debug(f'sentence_info: {sentence_info}')
        sentence_for_read = {}

        if sentence_info['order'] == 1:
            sentence_text = f'{self._title_book}\n\n{sentence_info["text"]}'
        else:
            sentence_text = sentence_info['text']

        sentence_for_read['sentence_id'] = sentence_info['sentence_id']
        sentence_for_read['book_id'] = sentence_info['book_id']
        sentence_for_read['text'] = sentence_text
        sentence_for_read['translation'] = sentence_info['translation']
        sentence_for_read['order'] = sentence_info['order']
        sentence_for_read['sentence_times'] = []
        sentence_for_read['description_time'] = []

        for tense in self._need_sentence.tenses:
            logger.debug(f'tense: {tense.__dict__}')
            sentence_for_read['sentence_times'].append(tense.name)
            sentence_for_read['description_time'].append(tense.short_description)

        sentence_for_read['sentence_times'] = ', '.join(sentence_for_read['sentence_times'])
        sentence_for_read['description_time'] = '\n'.join(sentence_for_read['description_time'])

        words_for_learn, words_for_sentence = await self._get_words_for_learn(words=sentence_info['words'])

        text_with_words = replace_with_translation(text=sentence_info['text'], words=words_for_sentence['all'])
        text_with_new_words = replace_with_translation(text=sentence_text, words=words_for_sentence['new'])

        sentence_for_read['text_with_words'] = text_with_words
        sentence_for_read['text_with_new_words'] = text_with_new_words
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

    async def _get_words_for_learn(self, words: list) -> tuple[list, dict]:
        """Get words for learn."""

        check_words = []

        if self._is_new_sentence is False:
            check_words = self._need_sentence.check_words or [0]

        words_for_learn = []
        words_for_sentence = {'all': [], 'new': []}
        for word in words:
            word_info = {}
            words_history = {}
            if word.users_words_history:
                words_history = word.users_words_history[0].__dict__

            is_known_word = words_history.get('is_known', False)

            words_for_sentence['all'].append(word)
            if is_known_word is False:
                words_for_sentence['new'].append(word)

            if check_words and word.word_id not in check_words:
                continue

            word_info['telegram_user_id'] = self._telegram_id
            word_info['word_id'] = word.word_id
            word_info['word'] = word.word
            word_info['type_word_id'] = word.type_word_id
            word_info['translation'] = word.translation
            word_info['is_known'] = is_known_word
            word_info['count_view'] = words_history.get('count_view', 0)
            word_info['correct_answers'] = words_history.get('correct_answers', 0)
            word_info['incorrect_answers'] = words_history.get('incorrect_answers', 0)
            word_info['correct_answers_in_row'] = words_history.get('correct_answers_in_row', 0)
            word_info['increase_factor'] = words_history.get('increase_factor', 0)
            word_info['interval_repeat'] = words_history.get('interval_repeat', 0)
            word_info['repeat_datetime'] = words_history.get('repeat_datetime', datetime.now())

            if word_info and is_known_word is False:
                words_for_learn.append(HistoryWordModelForReadDTO(**word_info).dict())

                if not words_history:
                    new_word = UsersWordsHistory(
                        telegram_user_id=word_info['telegram_user_id'],
                        word_id=word_info['word_id'],
                        is_known=word_info['is_known'],
                        count_view=word_info['count_view'],
                        correct_answers=word_info['correct_answers'],
                        incorrect_answers=word_info['incorrect_answers'],
                        correct_answers_in_row=word_info['correct_answers_in_row'],
                        repeat_datetime=datetime.utcnow(),
                    )
                    self._db.add(new_word)

            if is_known_word is True:
                continue

        return words_for_learn, words_for_sentence
