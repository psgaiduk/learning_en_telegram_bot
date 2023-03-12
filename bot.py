from os import path

from aiogram.utils import executor
from loguru import logger

from db.models import Base
from db.core import engine
from telegram_bot_app.core import dispatcher
from telegram_bot_app.handlers import *


file_path = path.join(path.dirname(__file__), 'logs', 'debug', 'logs.log')
logger.add(
    file_path,
    format="{time:YYYY-MM-DD HH:mm:ss} || {extra[chat_id]} || {extra[work_id]} || {level} || {message}",
    level="DEBUG",
    rotation='00:00',
)


if __name__ == '__main__':
    answer = input('enter command: ')
    if answer == '1':
        Base.metadata.create_all(bind=engine)
    executor.start_polling(dispatcher, skip_updates=True)
