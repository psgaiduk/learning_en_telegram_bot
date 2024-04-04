from datetime import datetime
from math import ceil

from fastapi import Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from api.v1.history import version_1_history_router
from database import get_db
from dto.models import HistoryWordModelDTO
from dto.requests import CreateHistoryWordDTO, GetHistoryWordsDTO, UpdateHistoryWordDTO
from dto.responses import OneResponseDTO, PaginatedResponseDTO
from functions import patch_data
from models import Users, UsersWordsHistory, Words


@version_1_history_router.post(
    path='/words/',
    response_model=OneResponseDTO[HistoryWordModelDTO],
    responses={
        status.HTTP_404_NOT_FOUND: {'description': 'Telegram user or word not found.'},
        status.HTTP_400_BAD_REQUEST: {'description': 'User already know word.'},
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_history_word_for_telegram_id(request: CreateHistoryWordDTO, db: Session = Depends(get_db)):
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

    history_word_dto = await get_words_history_dto(history_word.__dict__)

    return OneResponseDTO(detail=history_word_dto)


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

    if request.is_known is not None:
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


@version_1_history_router.patch(
    path='/words/',
    response_model=OneResponseDTO[HistoryWordModelDTO],
    responses={
        status.HTTP_404_NOT_FOUND: {'description': 'Telegram user or word not found.'},
        status.HTTP_400_BAD_REQUEST: {'description': 'User early not see this word.'},
    },
    status_code=status.HTTP_200_OK,
)
async def update_history_word_for_telegram_id(request: UpdateHistoryWordDTO, db: Session = Depends(get_db)):
    """Update history book by history book id."""
    telegram_id = request.telegram_user_id
    word_id = request.word_id

    telegram_user = db.query(Users).filter(Users.telegram_id == telegram_id).first()
    if not telegram_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

    word = db.query(Words).filter(Words.word_id == word_id).first()
    if not word:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Word not found.')

    history_word = db.query(UsersWordsHistory).filter(
        UsersWordsHistory.telegram_user_id == telegram_id,
        UsersWordsHistory.word_id == word_id,
    ).first()

    if not history_word:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User early not see this word.')

    history_word = patch_data(object_from_db=history_word, request=request)
    history_word.updated_at = datetime.utcnow()
    db.commit()

    history_word = (
        db.query(UsersWordsHistory)
        .options(joinedload(UsersWordsHistory.word))
        .filter(UsersWordsHistory.word_id == word_id, UsersWordsHistory.telegram_user_id == telegram_id).first())

    history_word_dto = await get_words_history_dto(history_word.__dict__)

    return OneResponseDTO(detail=history_word_dto)


@version_1_history_router.get(
    path='/learn_words/{telegram_id}/',
    # response_model=list[HistoryWordModelDTO],
    responses={
        status.HTTP_404_NOT_FOUND: {'description': 'User not found.'},
    },
    status_code=status.HTTP_200_OK,
)
async def get_learn_words_by_telegram_id(
        telegram_id: int,
        db: Session = Depends(get_db),
):
    """
    Get history book by history book id.

    :param telegram_id: telegram id.
    :param db: session for db.
    """

    telegram_user = db.query(Users).filter(Users.telegram_id == telegram_id).first()
    if not telegram_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

    learn_words = (
        db.query(UsersWordsHistory)
        .options(joinedload(UsersWordsHistory.word))
        .filter(
            UsersWordsHistory.telegram_user_id == telegram_id,
            UsersWordsHistory.is_known == True,
            UsersWordsHistory.repeat_datetime <= func.now()
        ).limit(20)
    ).all()

    return learn_words


async def get_words_history_dto(words_history: dict) -> HistoryWordModelDTO:
    word_info = words_history['word'].__dict__
    words_history['type_word_id'] = word_info['type_word_id']
    words_history['word'] = word_info['word']
    words_history['translation'] = word_info['translation']

    return HistoryWordModelDTO(**words_history)
