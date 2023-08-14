from fastapi import FastAPI

from books.api import v1_books_router


app = FastAPI()

app.include_router(v1_books_router)
