from aiogram.utils import executor

from telegram_bot_app.core import dispatcher
from telegram_bot_app.handlers import *


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
