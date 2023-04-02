from os import path

from aiogram.utils import executor
from loguru import logger

from telegram_bot_app.core import dispatcher
from telegram_bot_app.handlers import *


file_path = path.join(path.dirname(__file__), 'logs', 'debug', 'logs.log')
logger.add(
    file_path,
    format="{time:YYYY-MM-DD HH:mm:ss} || {extra[chat_id]} || {extra[work_id]} || {level} || {message}",
    level="DEBUG",
    rotation='00:00',
    retention='30 days'
)


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
