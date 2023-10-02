from http import HTTPStatus

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.storage import FSMContext

from context_managers import http_client
from settings import settings


class SetStateMiddleware(BaseMiddleware):

    _state: str

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        super(SetStateMiddleware, self).__init__()
        self._state = ''

    async def on_pre_process_message(self, message: types.Message, data: dict):
        user = message.from_user.id
        telegram_id = message.chat.id
        url_get_user = f'{settings.api_url}/v1/telegram_user/{telegram_id}'
        self._message = message

        async with http_client() as client:
            response = await client.get(url=url_get_user, headers=settings.api_headers)
            if response.status == HTTPStatus.NOT_FOUND:
                self._state = 'REGISTRATION'
            else:
                self._state = (await response.json())['detail']['stage']

        state = await self.get_real_state()

        storage = self.dispatcher.storage
        fsm_context = FSMContext(storage=storage, chat=telegram_id, user=user)
        await fsm_context.set_state(state=state)

    async def get_real_state(self):
        if self._state in {'CHECK_WORDS', 'REGISTRATION', 'GRAMMAR'}:
            return self._state

        return self._state


