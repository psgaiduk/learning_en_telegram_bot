from http import HTTPStatus

from aiogram import types, dispatcher as aiogram_dispatcher
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.storage import FSMContext

from choices import State
from context_managers import http_client
from dto import TelegramUserDTOModel
from functions import update_user
from settings import settings


class SetStateMiddleware(BaseMiddleware):
    """Set state middleware."""

    _state: str
    _message_text: str
    _telegram_user: TelegramUserDTOModel

    def __init__(self, dispatcher: aiogram_dispatcher) -> None:
        """Init."""
        self.dispatcher = dispatcher
        super(SetStateMiddleware, self).__init__()
        self._state = ''

    async def set_state_data(self, user, telegram_id) -> None:
        url_get_user = f'{settings.api_url}/v1/telegram_user/{telegram_id}'

        async with http_client() as client:
            response, response_status = await client.get(url=url_get_user, headers=settings.api_headers)
            if response_status == HTTPStatus.NOT_FOUND:
                self._state = State.registration.value
            elif response_status == HTTPStatus.OK:
                response_data = response['detail']
                self._state = response_data['stage']
            else:
                self._state = State.error.value

        if response_status == HTTPStatus.OK:
            self._telegram_user = TelegramUserDTOModel(**response_data)

        state = await self.get_real_state()
        storage = self.dispatcher.storage
        fsm_context = FSMContext(storage=storage, chat=telegram_id, user=user)

        if response_status == HTTPStatus.OK:
            await fsm_context.set_data(data={'user': self._telegram_user})

        await fsm_context.set_state(state=state)

    async def on_pre_process_message(self, message: types.Message, data: dict) -> None:
        """Set state for message."""
        self._message_text = message.text
        await self.set_state_data(message.from_user.id, message.chat.id)

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict) -> None:
        """Set state for callback_query."""
        self._message_text = callback_query.data
        await self.set_state_data(callback_query.from_user.id, callback_query.message.chat.id)

    async def get_real_state(self) -> str:
        """Get real state."""
        if self._state in {State.check_words.value, State.registration.value, State.grammar.value}:
            return self._state

        if self._message_text == '/profile':
            if self._telegram_user.stage == State.read_book.value:

                params_for_update = {
                    'telegram_id': self._telegram_user.telegram_id,
                    'previous_stage': self._telegram_user.stage,
                }

                is_update = await update_user(
                    telegram_id=self._telegram_user.telegram_id,
                    params_for_update=params_for_update,
                )
                if is_update is False:
                    return ''
            return State.update_profile.value

        if self._state != State.update_profile.value and self._message_text in {'/records', '/achievements'}:
            if self._message_text == '/records':
                return State.records.value
            return State.achievements.value

        return self._state
