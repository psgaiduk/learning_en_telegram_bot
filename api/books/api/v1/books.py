from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from database import get_db
from books.models import BooksModel
from app.decorators import api_key_required


v1_books_router = APIRouter()


@v1_books_router.get('/api/v1/book/{telegram_id}')
@api_key_required
async def get_random_book_for_user(request: Request, telegram_id: int, db: Session = Depends(get_db)):
    books = db.query(BooksModel).all()
    return [{"book_id": book.book_id, "title": book.title, "author": book.author} for book in books]
