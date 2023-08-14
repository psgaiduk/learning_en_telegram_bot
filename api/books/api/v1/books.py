from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from books.models import BooksModel
from main.decorators import api_key_required


v1_books_router = APIRouter()


@router.get('/api/v1/books')
@api_key_required
def get_random_book_for_user(db: Session = Depends(get_db)):
    books = db.query(BooksModel).all()
    return [{"book_id": book.book_id, "title": book.title, "author": book.author} for book in books]
