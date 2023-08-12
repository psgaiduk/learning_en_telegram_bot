from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from books.models import BooksModel
from database import get_db

app = FastAPI()

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    query = select(BooksModel)  # Создаем запрос на получение всех книг
    result = db.execute(query)  # Выполняем запрос
    books = result.fetchall()

    print(books)

    # Преобразуем результаты в список словарей
    return {'message': 'Hello world!'}
