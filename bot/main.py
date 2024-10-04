from aiogram.utils import executor
from sentry_sdk import init as sentry_init

from bot import dispatcher
from commands import *  # noqa F401, F403
from middlewears import SetStateMiddleware
from settings import settings


if settings.environment == "prod":
    sentry_init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )


dispatcher.middleware.setup(SetStateMiddleware(dispatcher))

if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)
