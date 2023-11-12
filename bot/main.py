from aiogram.utils import executor

from bot import dispatcher
from commands import *  # noqa F401, F403
from middlewears import SetStateMiddleware


dispatcher.middleware.setup(SetStateMiddleware(dispatcher))

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
