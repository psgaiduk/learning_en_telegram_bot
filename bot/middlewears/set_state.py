from http import HTTPStatus

from aiohttp import ClientSession
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.storage import FSMContext
from aiogram import types

from settings import settings


class SetStateMiddleware(BaseMiddleware):

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        super(SetStateMiddleware, self).__init__()
        
    async def on_pre_process_message(self, message: types.Message, data: dict):
        user = message.from_user.id
        telegram_id = message.chat.id
        url_get_user = f'{settings.api_url}/v1/telegram_user/{telegram_id}'

        async with ClientSession() as session:
            async with session.get(url_get_user, headers=settings.api_headers) as response:
                if response.status == HTTPStatus.NOT_FOUND:
                    state = 'REGISTRATION'
                else:
                    state = (await response.json())['detail']['stage']

        storage = self.dispatcher.storage
        fsm_context = FSMContext(storage=storage, chat=telegram_id, user=user)
        await fsm_context.set_state(state=state)
