from http import HTTPStatus
from typing import Optional

from aiogram import types, dispatcher as aiogram_dispatcher
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.storage import FSMContext
from loguru import logger

from choices import State
from context_managers import http_client
from dto import TelegramUserDTOModel, NewSentenceDTOModel, WordDTOModel
from functions import update_data_by_api
from settings import settings


class SetStateMiddleware(BaseMiddleware):
    """Set state middleware."""

    _state: str
    _message_text: str
    _telegram_user: Optional[TelegramUserDTOModel]
    _telegram_id: int

    def __init__(self, dispatcher: aiogram_dispatcher) -> None:
        """Init."""
        self.dispatcher = dispatcher
        super(SetStateMiddleware, self).__init__()
        self._state = ""
        self._telegram_user = None

    async def on_pre_process_message(self, message: types.Message, data: dict) -> None:
        """Set state for message."""
        self._message_text = message.text
        self._telegram_id = message.chat.id
        await self.get_fsm_context()
        await self._get_current_state()
        await self.set_state_data()

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict) -> None:
        """Set state for callback_query."""
        self._message_text = callback_query.data
        self._telegram_id = callback_query.message.chat.id
        await self.get_fsm_context()
        await self._get_current_state()
        await self.set_state_data()

    async def get_fsm_context(self) -> None:
        storage = self.dispatcher.storage
        self._fsm_context = FSMContext(storage=storage, chat=self._telegram_id, user=self._telegram_id)

    async def set_state_data(self) -> None:

        data = await self._fsm_context.get_data()
        logger.debug(f"context data = {data}")

        if self._telegram_user:
            await self._fsm_context.update_data(telegram_user=self._telegram_user)

        await self._fsm_context.set_state(state=self._state)

        data = await self._fsm_context.get_data()
        logger.debug(f"context data updated = {data}")

    async def _get_current_state(self) -> None:
        logger.debug("Get current state")
        url_get_user = f"{settings.api_url}/v1/telegram_user/{self._telegram_id}"

        async with http_client() as client:
            response, response_status = await client.get(url=url_get_user, headers=settings.api_headers)
            if response_status == HTTPStatus.NOT_FOUND:
                logger.debug("It is new user, start registration")
                self._state = State.registration.value
            elif response_status == HTTPStatus.OK:
                logger.debug("it is current user")
                await self.get_telegram_user(response=response)
                await self.update_telegram_user()
                await self.get_real_state()
            else:
                logger.debug("Get error from api")
                self._state = State.error.value

    async def get_telegram_user(self, response: dict) -> None:
        logger.debug("Get telegram user")
        response_data = response["detail"]
        self._state = response_data["stage"]
        self._telegram_user = TelegramUserDTOModel(**response_data)
        logger.debug(f"telegram_user = {self._telegram_user}")

    async def update_telegram_user(self) -> None:
        logger.debug("update telegram user")
        self._current_data = await self._fsm_context.get_data()
        logger.debug(f"Current state data: {self._current_data}")
        current_user: TelegramUserDTOModel = self._current_data.get("telegram_user")
        if current_user and current_user.new_sentence:
            logger.debug("We have current user and he has sentence insert new_sentence for him")
            self._telegram_user.new_sentence = current_user.new_sentence
            logger.debug(f"new_sentence = {self._telegram_user.new_sentence}")
        if current_user and current_user.learn_words:
            logger.debug("We have current user and he has learn words insert learn words for him")
            self._telegram_user.learn_words = current_user.learn_words
            logger.debug(f"learn_words = {self._telegram_user.learn_words}")
        logger.debug(f"Final update telegram_user = {self._telegram_user}")

    async def get_real_state(self) -> None:
        """Get real state."""
        if self._state in {State.grammar.value, State.update_profile.value, State.show_word.value}:
            logger.debug("It is grammar, update profile or show_word. End work.")
            return

        if self._message_text in {"/profile", "/records", "/achievements"}:
            logger.debug("It is one of commands. '/profile', '/records', '/achievements'")
            return await self._work_with_message_text()

        if self._state == State.start_learn_words.value or self._message_text == "learn_words_again":
            logger.debug("It is start learn words")
            self._state = await self._work_with_start_learn_words_status()
            return

        elif self._state == State.learn_words.value and len(self._telegram_user.learn_words) < 2:
            logger.debug("It is learn words and words 1 or less.")
            self._telegram_user.new_sentence = None
            self._state = State.read_book.value
            logger.debug("update sentence on '' and state for read book")

        if self._state in {State.read_book.value, State.check_answer_time.value}:
            logger.debug("It is read book or check answer time")
            self._state = await self.work_with_read_status()

        return

    async def _work_with_message_text(self) -> None:
        if self._message_text == "/profile":
            is_update = await self._update_state()
            if is_update is False:
                self._state = State.error.value
            else:
                self._state = State.update_profile.value
        elif self._message_text == "/records":
            self._state = State.records.value
        elif self._message_text == "/achievements":
            self._state = State.achievements.value

    async def _update_state(self) -> bool:
        if self._telegram_user.stage in {
            State.read_book.value,
            State.check_answer_time.value,
        }:
            params_for_update = {
                "telegram_id": self._telegram_user.telegram_id,
                "previous_stage": self._telegram_user.stage,
            }

            is_update = await update_data_by_api(
                telegram_id=self._telegram_user.telegram_id,
                params_for_update=params_for_update,
                url_for_update=f"telegram_user/{self._telegram_user.telegram_id}",
            )
            return is_update
        return True

    async def work_with_read_status(self) -> None:
        """Work with read status."""
        logger.debug(f"Start work_with_read_status: {self._state}")

        if self._telegram_user.new_sentence:
            logger.debug("user has sentence")
            if self._state == State.check_answer_time.value:
                logger.debug("It is check answer time return this state")
                return State.check_answer_time.value
            if self._telegram_user.new_sentence.words:
                logger.debug("User has words in sentence return check words")
                return State.check_words.value
            if self._telegram_user.new_sentence.text:
                logger.debug("User has text return read book")
                return State.read_book.value

        logger.debug("User does not have sentence")
        return await self._get_new_sentence()

    async def _work_with_start_learn_words_status(self) -> str:
        """Work with learn words status."""
        logger.debug(f"user without learn_words: {self._telegram_user.learn_words}")
        url_get_words_for_learn = f"{settings.api_url}/v1/history/learn-words/{self._telegram_user.telegram_id}/"
        async with http_client() as client:
            words_for_learn, response_status = await client.get(
                url=url_get_words_for_learn,
                headers=settings.api_headers,
            )
            logger.debug(f"words_for_learn: {words_for_learn}, status: {response_status}")
            if response_status != HTTPStatus.OK:
                logger.debug("learn words status is not ok, return error")
                return State.error.value

            if not words_for_learn:
                logger.debug("User does not have words for learn")
                self._state = State.read_book.value
                return await self.work_with_read_status()

            logger.debug("User has words for learn, add them to user.")
            self._telegram_user.learn_words = [WordDTOModel(**word) for word in words_for_learn]
            logger.debug(f"user learn_words: {self._telegram_user.learn_words}")

        logger.debug(f"User already learned words: {self._telegram_user.learn_words}")
        return State.start_learn_words.value

    async def _get_new_sentence(self) -> str:
        logger.debug("Get new sentence by api")
        url_get_new_sentence = f"{settings.api_url}/v1/read/{self._telegram_user.telegram_id}/"
        async with http_client() as client:
            response, response_status = await client.get(url=url_get_new_sentence, headers=settings.api_headers)
            if response_status == HTTPStatus.PARTIAL_CONTENT and self._state != State.check_answer_time.value:
                logger.debug("It is last sentence for today.")
                return State.read_book_end.value

            if response_status != HTTPStatus.OK and response_status != HTTPStatus.PARTIAL_CONTENT:
                logger.debug("It is error with api return error")
                return State.error.value
            new_sentence = response["detail"]
            logger.debug(f"new sentence = {new_sentence}")
            self._telegram_user.new_sentence = NewSentenceDTOModel(**new_sentence)
            logger.debug(f"update sentence for telegram user {self._telegram_user.new_sentence}")
            if self._state == State.check_answer_time.value:
                logger.debug("check answer time.")
                return State.check_answer_time.value
            if new_sentence["words"]:
                logger.debug("sentence have words return check words")
                return State.check_words.value
            logger.debug("return read book")
            return State.read_book.value
