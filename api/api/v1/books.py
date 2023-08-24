from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from database import get_db
from dto.models import BooksModelDTO
from functions import api_key_required
from models import BooksModel, BooksSentences, Users, UsersBooksHistory


version_1_books_router = APIRouter(
    prefix='/api/v1/books',
    tags=['Books'],
    dependencies=[Depends(api_key_required)],
    responses={status.HTTP_401_UNAUTHORIZED: {'description': 'Invalid API Key'}},
)


async def get_book_dto(book: BooksModel) -> BooksModelDTO:
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    book_dict = book.__dict__
    book_dict['books_sentences'] = [sentence.__dict__ for sentence in book.books_sentences]
    for sentence in book_dict['books_sentences']:
        sentence['words'] = [word.__dict__ for word in sentence['words']]

    return BooksModelDTO(**book_dict)


@version_1_books_router.get('/{book_id}/', response_model=BooksModelDTO)
async def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    """Get book by id."""
    book = (
        db.query(BooksModel)
        .options(joinedload(BooksModel.books_sentences).joinedload(BooksSentences.words))
        .filter(BooksModel.book_id == book_id)
        .first()
    )

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    return await get_book_dto(book)


@version_1_books_router.get('/get-random-book/{telegram_id}/', response_model=BooksModelDTO)
async def get_random_book_by_telegram_id(telegram_id: int, db: Session = Depends(get_db)):
    """Get random book by telegram id."""

    user_level_id = (
        db.query(Users.level_en_id)
        .filter(Users.telegram_id == telegram_id)
        .scalar()
    )

    if not user_level_id:
        raise ValueError('User does not have a level_en_id.')

    read_books = (
        db.query(UsersBooksHistory.book_id)
        .filter(UsersBooksHistory.telegram_user_id == telegram_id)
        .subquery()
    )

    random_book = (
        db.query(BooksModel)
        .options(joinedload(BooksModel.books_sentences).joinedload(BooksSentences.words))
        .filter(
            BooksModel.level_en_id == user_level_id,
            ~BooksModel.book_id.in_(read_books)
        )
        .order_by(func.random())
        .first()
    )

    if not random_book:
        return None

    return await get_book_dto(book=random_book)



