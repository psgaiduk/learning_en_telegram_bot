from aiogram.utils import executor

from bot import dispatcher
from commands import *


if __name__ == '__main__':
    print('start work')
    executor.start_polling(dispatcher, skip_updates=True)
