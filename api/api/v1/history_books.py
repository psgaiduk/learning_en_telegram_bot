from datetime import datetime

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from api.v1.books import get_book_dto
from api.v1.history import version_1_history_router
from database import get_db
from dto.models import BooksHistoryModelDTO
from models import UsersBooksHistory, BooksModel, BooksSentences, Users


async def get_history_book_dto(
    user_history_book_db: UsersBooksHistory,
) -> BooksHistoryModelDTO:
    user_history_book_dict = user_history_book_db.__dict__
    user_history_book_dict["book"] = await get_book_dto(user_history_book_db.book)
    user_history_book = BooksHistoryModelDTO(**user_history_book_dict)

    return user_history_book


async def get_book(history_book_id: int, db: Session = Depends(get_db)):
    """
    Get book by history book id.

    :param history_book_id: history book id.
    :param db: session for connect to db.
    :return: book model dto.
    """

    user_history_book_db = (
        db.query(UsersBooksHistory)
        .options(
            joinedload(UsersBooksHistory.book).joinedload(BooksModel.books_sentences).joinedload(BooksSentences.words)
        )
        .filter(UsersBooksHistory.id == history_book_id)
        .first()
    )

    if not user_history_book_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History book not found.")

    return await get_history_book_dto(user_history_book_db=user_history_book_db)


@version_1_history_router.post(
    path="/books/{telegram_id}/{book_id}",
    response_model=BooksHistoryModelDTO,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "User already read book."},
        status.HTTP_404_NOT_FOUND: {"description": "User or book not found."},
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_history_book_for_telegram_id(telegram_id: int, book_id, db: Session = Depends(get_db)):
    """Add history book for telegram id."""

    telegram_user = db.query(Users).filter(Users.telegram_id == telegram_id).first()
    if not telegram_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    start_read_book = (
        db.query(UsersBooksHistory)
        .filter(
            UsersBooksHistory.telegram_user_id == telegram_id,
            UsersBooksHistory.end_read.is_(None),
        )
        .first()
    )

    if start_read_book:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already read book.")

    book = db.query(BooksModel).filter(BooksModel.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")

    new_history_book = UsersBooksHistory(telegram_user_id=telegram_id, book_id=book_id)
    db.add(new_history_book)
    db.commit()

    return await get_book(new_history_book.id, db)


@version_1_history_router.patch(
    path="/books/{history_book_id}",
    response_model=BooksHistoryModelDTO,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "History book not found."},
    },
    status_code=status.HTTP_200_OK,
)
async def complete_read_book(history_book_id: int, db: Session = Depends(get_db)):
    """Update history book."""

    history_book_id = db.query(UsersBooksHistory).filter(UsersBooksHistory.id == history_book_id).first()
    if not history_book_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History book not found.")

    history_book_id.end_read = datetime.now()
    db.commit()

    return await get_book(history_book_id=history_book_id.id, db=db)


@version_1_history_router.get(
    path="/books/{history_book_id}",
    response_model=BooksHistoryModelDTO,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "History book not found."},
    },
    status_code=status.HTTP_200_OK,
)
async def get_history_read_book(history_book_id: int, db: Session = Depends(get_db)):
    """Get history book by history book id."""

    history_book_id = db.query(UsersBooksHistory).filter(UsersBooksHistory.id == history_book_id).first()
    if not history_book_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History book not found.")

    return await get_book(history_book_id=history_book_id.id, db=db)


@version_1_history_router.get(
    path="/books/telegram_user/{telegram_id}",
    response_model=list[BooksHistoryModelDTO],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "History book for user not found."},
    },
    status_code=status.HTTP_200_OK,
)
async def get_history_read_books_for_user(telegram_id: int, db: Session = Depends(get_db)):
    """Get history book by history book id."""

    user_history_books = (
        db.query(UsersBooksHistory)
        .options(
            joinedload(UsersBooksHistory.book).joinedload(BooksModel.books_sentences).joinedload(BooksSentences.words)
        )
        .filter(UsersBooksHistory.telegram_user_id == telegram_id)
        .all()
    )

    if not user_history_books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="History book for user not found.",
        )

    return [await get_history_book_dto(user_history_book_db=history_book) for history_book in user_history_books]
