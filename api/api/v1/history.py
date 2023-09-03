from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from api.v1.books import get_book_dto
from functions import api_key_required
from database import get_db
from dto.models import BooksHistoryModelDTO
from models import UsersBooksHistory, BooksModel, BooksSentences, Users


version_1_history_router = APIRouter(
    prefix='/api/v1/history',
    tags=['History'],
    dependencies=[Depends(api_key_required)],
    responses={status.HTTP_401_UNAUTHORIZED: {'description': 'Invalid API Key'}},
)


@version_1_history_router.post(
    path='/books/{telegram_id}/{book_id}', 
    response_model=BooksHistoryModelDTO,
    responses={
        status.HTTP_400_BAD_REQUEST: {'description': 'User already read book.'},
        status.HTTP_404_NOT_FOUND: {'description': 'User or book not found.'},
    }
)
async def add_history_book_for_telegram_id(telegram_id: int, book_id, db: Session = Depends(get_db)):
    """Add history book for telegram id."""

    telegram_user = db.query(Users).filter(Users.telegram_id == telegram_id).first()
    if not telegram_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

    start_read_book = db.query(UsersBooksHistory).filter(
        UsersBooksHistory.telegram_user_id == telegram_id,
        UsersBooksHistory.end_read is None,
    ).first()

    if start_read_book:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already read book.')

    book = db.query(BooksModel).filter(BooksModel.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found.')

    new_history_book = UsersBooksHistory(telegram_user_id=telegram_id, book_id=book_id)
    db.add(new_history_book)
    db.commit()

    user_history_book_db = (
        db.query(UsersBooksHistory)
        .options(joinedload(UsersBooksHistory.book)
                 .joinedload(BooksModel.books_sentences)
                 .joinedload(BooksSentences.words))
        .filter(UsersBooksHistory.telegram_user_id == telegram_id, UsersBooksHistory.book_id == book_id)
        .first()
    )

    if not user_history_book_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='History book not found.')

    user_history_book_dict = user_history_book_db.__dict__
    user_history_book_dict['book'] = await get_book_dto(user_history_book_db.book)
    user_history_book = BooksHistoryModelDTO(**user_history_book_dict)

    return user_history_book
