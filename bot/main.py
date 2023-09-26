from aiogram.utils import executor

from bot import dispatcher
from commands import *
from middlewears import SetStateMiddleware


dispatcher.middleware.setup(SetStateMiddleware(dispatcher))

if __name__ == '__main__':
    print('start work')
    executor.start_polling(dispatcher, skip_updates=True)
