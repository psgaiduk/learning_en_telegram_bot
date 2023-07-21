from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.settings import settings

bot = Bot(token=settings.telegram_token)

storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)
