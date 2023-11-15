from fastapi import FastAPI
from sentry_sdk import init as sentry_init

from api import (
    version_1_telegram_user_router,
    version_1_service_router,
    version_1_books_router,
    version_1_history_router,
    version_1_referral_router,
    version_1_read_router,
)
from settings import settings


if settings.environment == 'prod':
    sentry_init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

app = FastAPI()

app.include_router(version_1_telegram_user_router)
app.include_router(version_1_service_router)
app.include_router(version_1_books_router)
app.include_router(version_1_history_router)
app.include_router(version_1_referral_router)
app.include_router(version_1_read_router)
