from fastapi import FastAPI

from api import version_1_telegram_user_router


app = FastAPI()

app.include_router(version_1_telegram_user_router)
