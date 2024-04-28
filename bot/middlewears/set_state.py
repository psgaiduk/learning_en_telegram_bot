from http import HTTPStatus
from typing import Optional

from aiogram import types, dispatcher as aiogram_dispatcher
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.storage import FSMContext
from loguru import logger

from choices import State
from context_managers import http_client
from dto import TelegramUserDTOModel, NewSentenceDTOModel
from functions import update_data_by_api
from settings import settings


class SetStateMiddleware(BaseMiddleware):
    """Set state middleware."""

    _state: str
    _message_text: str
    _telegram_user: Optional[TelegramUserDTOModel]

    def __init__(self, dispatcher: aiogram_dispatcher) -> None:
        """Init."""
        self.dispatcher = dispatcher
        super(SetStateMiddleware, self).__init__()
        self._state = ''
        self._telegram_user = None

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

        storage = self.dispatcher.storage
        fsm_context = FSMContext(storage=storage, chat=telegram_id, user=user)
        self._current_data = await fsm_context.get_data()
        logger.debug(f'Current state data: {self._current_data}')

        if response_status == HTTPStatus.OK:
            self._telegram_user = TelegramUserDTOModel(**response_data)
            logger.debug(f'current data: {self._current_data}, telegram_user = {self._telegram_user}')
            current_user: TelegramUserDTOModel = self._current_data.get('user')
            if current_user and current_user.new_sentence:
                self._telegram_user.new_sentence = current_user.new_sentence

        state = await self.get_real_state()

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
        if self._state in {State.registration.value, State.grammar.value, State.error.value}:
            return self._state

        conditions_for_update_profile = {
            self._message_text == '/profile',
            self._telegram_user.stage in {State.read_book.value, State.check_answer_time.value}
        }

        if all(conditions_for_update_profile):

            params_for_update = {
                'telegram_id': self._telegram_user.telegram_id,
                'previous_stage': self._telegram_user.stage,
            }

            is_update = await update_data_by_api(
                telegram_id=self._telegram_user.telegram_id,
                params_for_update=params_for_update,
                url_for_update=f'telegram_user/{self._telegram_user.telegram_id}',
            )
            if is_update is False:
                return State.error.value
            return State.update_profile.value

        elif self._state != State.update_profile.value and self._message_text == '/records':
            return State.records.value
        elif self._state != State.update_profile.value and self._message_text == '/achievements':
            return State.achievements.value

        if self._state == State.start_learn_words.value:
            await self._work_with_start_learn_words_status()

        if self._state in {State.read_book.value, State.check_answer_time.value}:
            return await self.work_with_read_status()

        return self._state

    async def work_with_read_status(self) -> str:
        """Work with read status."""
        logger.debug(f'work_with_read_status: {self._state}')

        if self._telegram_user.new_sentence:
            if self._state == State.check_answer_time.value:
                return State.check_answer_time.value
            if self._telegram_user.new_sentence.words:
                return State.check_words.value
            if self._telegram_user.new_sentence.text:
                return State.read_book.value

        url_get_new_sentence = f'{settings.api_url}/v1/read/{self._telegram_user.telegram_id}/'
        async with http_client() as client:
            response, response_status = await client.get(url=url_get_new_sentence, headers=settings.api_headers)
            if response_status == HTTPStatus.PARTIAL_CONTENT and self._state != State.check_answer_time.value:
                return State.read_book_end.value
            elif response_status != HTTPStatus.OK:
                return State.error.value

            new_sentence = response['detail']
            self._telegram_user.new_sentence = NewSentenceDTOModel(**new_sentence)
            if self._state == State.check_answer_time.value:
                return State.check_answer_time.value
            if new_sentence['words']:
                return State.check_words.value
            return State.read_book.value

    async def _work_with_start_learn_words_status(self) -> str:
        """Work with learn words status."""

        logger.debug(f'user without learn_words: {self._telegram_user.learn_words}')
        url_get_words_for_learn = f'{settings.api_url}/v1/history/learn-words/{self._telegram_user.telegram_id}/'
        async with http_client() as client:
            words_for_learn, response_status = await client.get(
                url=url_get_words_for_learn,
                headers=settings.api_headers,
            )
            logger.debug(f'words_for_learn: {words_for_learn}, status: {response_status}')
            if response_status != HTTPStatus.OK:
                logger.debug('learn words status is not ok, return error')
                return State.error.value

            if not words_for_learn:
                logger.debug('User does not have words for learn')
                return State.read_book.value

            logger.debug('User has words for learn, add them to user.')
            self._telegram_user.learn_words = words_for_learn
            logger.debug(f'user learn_words: {self._telegram_user.learn_words}')

        logger.debug(f'User already learned words: {self._telegram_user.learn_words}')
        return State.start_learn_words.value
