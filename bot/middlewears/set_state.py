from http import HTTPStatus

from aiogram import types, dispatcher as aiogram_dispatcher
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.storage import FSMContext

from choices import State
from context_managers import http_client
from dto import TelegramUserDTOModel
from settings import settings


class SetStateMiddleware(BaseMiddleware):
    """Set state middleware."""

    _state: str
    _message: types.Message

    def __init__(self, dispatcher: aiogram_dispatcher) -> None:
        """Init."""
        self.dispatcher = dispatcher
        super(SetStateMiddleware, self).__init__()
        self._state = ''

    async def on_pre_process_message(self, message: types.Message, data: dict) -> None:
        """Set state."""
        user = message.from_user.id
        telegram_id = message.chat.id
        url_get_user = f'{settings.api_url}/v1/telegram_user/{telegram_id}'
        self._message = message

        async with http_client() as client:
            response, response_status = await client.get(url=url_get_user, headers=settings.api_headers)
            if response_status == HTTPStatus.NOT_FOUND:
                self._state = State.registration.value
            elif response_status == HTTPStatus.OK:
                response_data = response['detail']
                self._state = response_data['stage']
            else:
                self._state = State.error.value

        state = await self.get_real_state()

        storage = self.dispatcher.storage
        fsm_context = FSMContext(storage=storage, chat=telegram_id, user=user)

        if response_status == HTTPStatus.OK:
            await fsm_context.set_data(data={'user': TelegramUserDTOModel(**response_data)})

        await fsm_context.set_state(state=state)

    async def get_real_state(self) -> str:
        """Get real state."""
        if self._state in {State.check_words.value, State.registration.value, State.grammar.value}:
            return self._state

        if self._message.text == '/profile':
            return State.update_profile.value

        if self._state != State.update_profile.value and self._message.text in {'/records', '/achievements'}:
            if self._message.text == '/records':
                return State.records.value
            return State.achievements.value

        return self._state


