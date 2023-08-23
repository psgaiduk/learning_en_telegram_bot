from fastapi import FastAPI

from api import version_1_telegram_user_router, version_1_service_router, version_1_books_router


app = FastAPI()

app.include_router(version_1_telegram_user_router)
app.include_router(version_1_service_router)
app.include_router(version_1_books_router)
