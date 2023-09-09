from fastapi import Depends, HTTPException, status
from math import ceil
from sqlalchemy.orm import Session, joinedload

from api.v1.history import version_1_history_router
from database import get_db
from dto.models import CreateHistoryWordModelDTO, HistoryWordModelDTO
from dto.requests import GetHistoryWordsDTO
from dto.responses import PaginatedResponseDTO
from models import Users, UsersWordsHistory, Words


@version_1_history_router.post(
    path='/words/',
    response_model=HistoryWordModelDTO,
    responses={
        status.HTTP_404_NOT_FOUND: {'description': 'Telegram user or word not found.'},
        status.HTTP_400_BAD_REQUEST: {'description': 'User already know word.'},
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_history_word_for_telegram_id(request: CreateHistoryWordModelDTO, db: Session = Depends(get_db)):
    """Get history book by history book id."""

    telegram_id = request.telegram_user_id
    word_id = request.word_id

    telegram_user = db.query(Users).filter(Users.telegram_id == telegram_id).first()
    if not telegram_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

    word = db.query(Words).filter(Words.word_id == word_id).first()
    if not word:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Word not found.')

    old_history_word = db.query(UsersWordsHistory).filter(
        UsersWordsHistory.telegram_user_id == telegram_id,
        UsersWordsHistory.word_id == word_id,
    ).first()

    if old_history_word:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already know word.')

    new_history_word = UsersWordsHistory(
        telegram_user_id=telegram_id,
        word_id=word_id,
    )
    db.add(new_history_word)
    db.commit()

    history_word = (
        db.query(UsersWordsHistory)
        .options(joinedload(UsersWordsHistory.word))
        .filter(UsersWordsHistory.id == new_history_word.id).first())

    return await get_words_history_dto(history_word.__dict__)


@version_1_history_router.get(
    path='/words/{telegram_id}/',
    response_model=PaginatedResponseDTO[HistoryWordModelDTO],
    responses={
        status.HTTP_404_NOT_FOUND: {'description': 'User not found.'},
    },
    status_code=status.HTTP_200_OK,
)
async def get_words_history_by_telegram_id(
        telegram_id: int,
        request: GetHistoryWordsDTO = Depends(),
        db: Session = Depends(get_db),
):
    """Get history book by history book id."""

    telegram_user = db.query(Users).filter(Users.telegram_id == telegram_id).first()
    if not telegram_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

    if request.page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Page must be greater than zero.')
    if request.limit < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Limit must be greater than zero.')
    if request.limit > 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Limit must be less than 200.')

    query = (
        db.query(UsersWordsHistory)
        .options(joinedload(UsersWordsHistory.word))
        .filter(UsersWordsHistory.telegram_user_id == telegram_id))

    if request.word_id:
        query = query.filter(UsersWordsHistory.word_id == request.word_id)

    if request.is_known:
        query = query.filter(UsersWordsHistory.is_known == request.is_known)

    if request.count_view_gte:
        query = query.filter(UsersWordsHistory.count_view >= request.count_view_gte)

    if request.count_view_lte:
        query = query.filter(UsersWordsHistory.count_view <= request.count_view_lte)
        
    if request.correct_answers_gte:
        query = query.filter(UsersWordsHistory.correct_answers >= request.correct_answers_gte)
        
    if request.correct_answers_lte:
        query = query.filter(UsersWordsHistory.correct_answers <= request.correct_answers_lte)

    if request.incorrect_answers_gte:
        query = query.filter(UsersWordsHistory.incorrect_answers >= request.incorrect_answers_gte)

    if request.incorrect_answers_lte:
        query = query.filter(UsersWordsHistory.incorrect_answers <= request.incorrect_answers_lte)

    if request.correct_answers_in_row_gte:
        query = query.filter(UsersWordsHistory.correct_answers_in_row >= request.correct_answers_in_row_gte)

    if request.correct_answers_in_row_lte:
        query = query.filter(UsersWordsHistory.correct_answers_in_row <= request.correct_answers_in_row_lte)

    skip = (request.page - 1) * request.limit
    total_count = query.count()
    total_pages = ceil(total_count / request.limit)
    history_words = query.offset(skip).limit(request.limit).all()
    per_page = len(history_words)

    results = [await get_words_history_dto(words_history=history_word.__dict__) for history_word in history_words]

    return PaginatedResponseDTO(
        results=results,
        page=request.page,
        per_page=per_page,
        total=total_count,
        total_pages=total_pages,
    )


async def get_words_history_dto(words_history: dict) -> HistoryWordModelDTO:
    word_info = words_history['word'].__dict__
    words_history['type_word_id'] = word_info['type_word_id']
    words_history['word'] = word_info['word']
    words_history['translation'] = word_info['translation']

    return HistoryWordModelDTO(**words_history)
