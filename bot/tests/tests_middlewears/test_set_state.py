from pytest import mark

from datetime import datetime

from aiogram.types import CallbackQuery, Chat, Message, User
from aiogram.dispatcher.storage import BaseStorage, FSMContext
from http import HTTPStatus
from unittest.mock import AsyncMock, Mock, patch

from choices import State
from dto import TelegramUserDTOModel, WordDTOModel
from middlewears import SetStateMiddleware
from settings import settings
from tests.fixtures import *


class TestSetStateMiddleware:
    """Tests for SetStateMiddleware."""

    def setup_method(self, sentence_with_word):
        self._chat = 12345
        self._user = 12345
        self._message = Mock()
        self._get_method_target = "context_managers.aio_http_client.AsyncHttpClient.get"
        self._storage_mock = Mock(spec=BaseStorage)
        self._service = SetStateMiddleware(dispatcher=Mock(storage=self._storage_mock))
        self._response_data = {
            "detail": {
                "stage": "",
                "user_name": "test_name",
                "experience": 0,
                "previous_stage": "",
                "telegram_id": 12345,
                "hero_level": None,
                "level_en": None,
                "main_language": None,
            }
        }
        self._new_sentence = sentence_with_word

    @mark.asyncio
    async def test_on_pre_process_message(self):
        expected_message = "test message"
        chat = Chat(id=self._chat)
        user = User(id=self._chat, is_bot=False, first_name="Test User")
        mock_message = Message(id=1, chat=chat, text=expected_message, from_user=user)
        mock_message.from_user = user

        mock_get_current_state = AsyncMock(return_value=None)
        self._service._get_current_state = mock_get_current_state
        mock_set_state_data = AsyncMock(return_value=None)
        self._service.set_state_data = mock_set_state_data
        mock_get_get_fsm_context = AsyncMock(return_value=None)
        self._service.get_fsm_context = mock_get_get_fsm_context

        await self._service.on_pre_process_message(message=mock_message, data={})

        assert self._service._message_text == expected_message
        assert self._service._telegram_id == self._chat
        mock_get_current_state.assert_called_once()
        mock_set_state_data.assert_called_once()
        mock_get_get_fsm_context.assert_called_once()

    @mark.asyncio
    async def test_on_pre_process_callback_query(self):
        expected_message = "test message"
        chat = Chat(id=self._chat)
        user = User(id=self._chat, is_bot=False, first_name="Test User")
        mock_callback = CallbackQuery(id=1, chat=chat, data=expected_message, from_user=user)
        mock_callback.from_user = user
        mock_callback.message = Message(id=1, chat=chat, text=expected_message, from_user=user)

        mock_get_current_state = AsyncMock(return_value=None)
        self._service._get_current_state = mock_get_current_state
        mock_set_state_data = AsyncMock(return_value=None)
        self._service.set_state_data = mock_set_state_data
        mock_get_get_fsm_context = AsyncMock(return_value=None)
        self._service.get_fsm_context = mock_get_get_fsm_context

        await self._service.on_pre_process_callback_query(callback_query=mock_callback, data={})

        assert self._service._message_text == expected_message
        assert self._service._telegram_id == self._chat
        mock_get_current_state.assert_called_once()
        mock_set_state_data.assert_called_once()
        mock_get_get_fsm_context.assert_called_once()

    @mark.asyncio
    async def test_set_state_data_with_telegram_user(self, mocker):

        telegram_user = TelegramUserDTOModel(**self._response_data["detail"])
        state = "state"
        self._service._telegram_user = telegram_user
        self._service._state = state

        fsm_context_mock = mocker.Mock(spec=FSMContext)
        fsm_context_mock.set_state = mocker.AsyncMock()
        fsm_context_mock.update_data = mocker.AsyncMock()
        self._service._fsm_context = fsm_context_mock

        await self._service.set_state_data()
        fsm_context_mock.set_state.assert_called_once_with(state=state)
        fsm_context_mock.update_data.assert_called_once_with(telegram_user=telegram_user)

    @mark.asyncio
    async def test_set_state_data_without_telegram_user(self, mocker):

        telegram_user = TelegramUserDTOModel(**self._response_data["detail"])
        state = "state"
        self._service._telegram_user = telegram_user
        self._service._state = state

        fsm_context_mock = mocker.Mock(spec=FSMContext)
        fsm_context_mock.set_state = mocker.AsyncMock()
        fsm_context_mock.set_data = mocker.AsyncMock()
        self._service._fsm_context = fsm_context_mock

        self._service._telegram_user = None
        await self._service.set_state_data()
        fsm_context_mock.set_state.assert_called_once_with(state=state)
        fsm_context_mock.set_data.assert_not_called()

    @mark.parametrize(
        "response_status, expected_state",
        [
            (HTTPStatus.NOT_FOUND, State.registration.value),
            (HTTPStatus.OK, "expected_stage_from_api"),
            (HTTPStatus.BAD_REQUEST, State.error.value),
        ],
    )
    @mark.asyncio
    async def test_get_current_state(self, response_status, expected_state):
        response_data = self._response_data
        response_data["detail"]["stage"] = expected_state

        self._service._state = ""
        self._service._telegram_id = self._chat
        mock_get_telegram_user = AsyncMock(return_value=None)
        self._service.get_telegram_user = mock_get_telegram_user
        mock_update_telegram_user = AsyncMock(return_value=None)
        self._service.update_telegram_user = mock_update_telegram_user
        mock_get_real_state = AsyncMock(return_value=None)
        self._service.get_real_state = mock_get_real_state

        with patch(self._get_method_target, return_value=(response_data, response_status)) as mocked_get:
            await self._service._get_current_state()

        mocked_get.assert_called_once_with(
            url=f"{settings.api_url}/v1/telegram_user/{self._chat}",
            headers=settings.api_headers,
        )

        if response_status == HTTPStatus.OK:
            mock_get_real_state.assert_called_once()
            mock_get_telegram_user.assert_called_once_with(response=response_data)
            mock_update_telegram_user.assert_called_once()
        else:
            mock_get_real_state.assert_not_called()
            mock_get_telegram_user.assert_not_called()
            mock_update_telegram_user.assert_not_called()
            assert self._service._state == expected_state

    @mark.parametrize("expected_stage", ["first", "second"])
    @mark.asyncio
    async def test_get_telegram_user(self, expected_stage):
        response = self._response_data
        response["detail"]["stage"] = expected_stage

        await self._service.get_telegram_user(response=response)

        assert isinstance(self._service._telegram_user, TelegramUserDTOModel)
        assert self._service._telegram_user.stage == expected_stage

    @mark.parametrize(
        "is_new_sentence, is_learn_words",
        [(False, False), (True, False), (False, True), (True, True)],
    )
    @mark.asyncio
    async def test_update_telegram_user(self, mocker, sentence_with_word, is_new_sentence, is_learn_words):
        telegram_user = TelegramUserDTOModel(**self._response_data["detail"])

        self._service._telegram_user = TelegramUserDTOModel(**self._response_data["detail"])

        if is_new_sentence:
            telegram_user.new_sentence = sentence_with_word
        if is_learn_words:
            telegram_user.learn_words = sentence_with_word.words

        assert self._service._telegram_user.new_sentence is None
        assert self._service._telegram_user.learn_words == []

        fsm_context_mock = mocker.Mock(spec=FSMContext)
        fsm_context_mock.get_data = mocker.AsyncMock(return_value={"telegram_user": telegram_user})
        self._service._fsm_context = fsm_context_mock

        await self._service.update_telegram_user()

        assert self._service._telegram_user.new_sentence == telegram_user.new_sentence
        assert self._service._telegram_user.learn_words == telegram_user.learn_words

    @mark.parametrize(
        "message_text, state, expected_state",
        [
            ("/profile", State.grammar.value, State.grammar.value),
            ("/profile", State.update_profile.value, State.update_profile.value),
            ("/records", State.grammar.value, State.grammar.value),
            ("/records", State.update_profile.value, State.update_profile.value),
            ("/achievements", State.grammar.value, State.grammar.value),
            ("/achievements", State.update_profile.value, State.update_profile.value),
            ("just text", State.update_profile.value, State.update_profile.value),
            ("just text", State.grammar.value, State.grammar.value),
        ],
    )
    @mark.asyncio
    async def test_get_real_state_grammar_and_update_profile(self, message_text, state, expected_state):
        self._service._state = state
        self._service._message_text = message_text
        self._service._telegram_user = TelegramUserDTOModel(**self._response_data["detail"])

        mock_work_with_message_text = AsyncMock(return_value=state)
        self._service._work_with_message_text = mock_work_with_message_text
        mock_work_with_start_learn_words_status = AsyncMock(return_value=state)
        self._service._work_with_start_learn_words_status = mock_work_with_start_learn_words_status
        mock_work_with_read_status = AsyncMock(return_value=state)
        self._service.work_with_read_status = mock_work_with_read_status

        await self._service.get_real_state()

        assert self._service._state == expected_state
        mock_work_with_message_text.assert_not_called()
        mock_work_with_read_status.assert_not_called()
        mock_work_with_start_learn_words_status.assert_not_called()

    @mark.parametrize(
        "message_text, state",
        [
            ("/profile", State.read_book.value),
            ("/profile", State.start_learn_words.value),
            ("/profile", State.learn_words.value),
            ("/records", State.read_book.value),
            ("/records", State.start_learn_words.value),
            ("/records", State.learn_words.value),
            (
                "/achievements",
                State.read_book.value,
            ),
            ("/achievements", State.start_learn_words.value),
            ("/achievements", State.learn_words.value),
        ],
    )
    @mark.asyncio
    async def test_get_real_state_with_specific_text(self, message_text, state):
        self._service._state = state
        self._service._message_text = message_text
        self._service._telegram_user = TelegramUserDTOModel(**self._response_data["detail"])

        mock_work_with_message_text = AsyncMock(return_value=state)
        self._service._work_with_message_text = mock_work_with_message_text
        mock_work_with_start_learn_words_status = AsyncMock(return_value=state)
        self._service._work_with_start_learn_words_status = mock_work_with_start_learn_words_status
        mock_work_with_read_status = AsyncMock(return_value=state)
        self._service.work_with_read_status = mock_work_with_read_status

        await self._service.get_real_state()

        mock_work_with_message_text.assert_awaited_once()
        mock_work_with_read_status.assert_not_called()
        mock_work_with_start_learn_words_status.assert_not_called()

    @mark.parametrize(
        "message_text, state",
        [
            ("some text", State.start_learn_words.value),
            ("random text", State.start_learn_words.value),
            ("just text", State.start_learn_words.value),
            ("learn_words_again", State.read_book.value),
            ("learn_words_again", State.read_book_end.value),
        ],
    )
    @mark.asyncio
    async def test_get_real_state_start_learn_words(self, message_text, state):
        self._service._state = state
        self._service._message_text = message_text
        self._service._telegram_user = TelegramUserDTOModel(**self._response_data["detail"])

        mock_work_with_message_text = AsyncMock(return_value=state)
        self._service._work_with_message_text = mock_work_with_message_text
        mock_work_with_start_learn_words_status = AsyncMock(return_value=state)
        self._service._work_with_start_learn_words_status = mock_work_with_start_learn_words_status
        mock_work_with_read_status = AsyncMock(return_value=state)
        self._service.work_with_read_status = mock_work_with_read_status

        await self._service.get_real_state()

        mock_work_with_message_text.assert_not_called()
        mock_work_with_read_status.assert_not_called()
        mock_work_with_start_learn_words_status.assert_called_once()

    @mark.parametrize(
        "message_text, state, count_words",
        [
            ("some text", State.learn_words.value, 3),
            ("random text", State.learn_words.value, 2),
            ("just text", State.learn_words.value, 1),
            ("just text", State.learn_words.value, 0),
        ],
    )
    @mark.asyncio
    async def test_get_real_state_learn_words(self, message_text, state, count_words):
        self._service._state = state
        self._service._message_text = message_text
        self._service._telegram_user = TelegramUserDTOModel(**self._response_data["detail"])
        word_dto = WordDTOModel(
            word_id=1,
            word="test",
            type_word_id=1,
            transcription="test",
            part_of_speech="n",
            is_known=True,
            count_view=0,
            correct_answers=0,
            incorrect_answers=0,
            correct_answers_in_row=0,
            increase_factor=0,
            interval_repeat=0,
            repeat_datetime=datetime.now(),
        )
        self._service._telegram_user.learn_words = [word_dto for _ in range(count_words)]

        mock_work_with_message_text = AsyncMock(return_value=state)
        self._service._work_with_message_text = mock_work_with_message_text
        mock_work_with_start_learn_words_status = AsyncMock(return_value=state)
        self._service._work_with_start_learn_words_status = mock_work_with_start_learn_words_status
        mock_work_with_read_status = AsyncMock(return_value=state)
        self._service.work_with_read_status = mock_work_with_read_status

        await self._service.get_real_state()

        mock_work_with_message_text.assert_not_called()
        mock_work_with_start_learn_words_status.assert_not_called()
        if count_words < 2:
            mock_work_with_read_status.assert_called_once()
        else:
            mock_work_with_read_status.assert_not_called()

    @mark.parametrize(
        "message_text, state",
        [
            ("some text", State.read_book.value),
            ("random text", State.check_answer_time.value),
        ],
    )
    @mark.asyncio
    async def test_get_real_state_work_with_read_status(self, message_text, state):
        self._service._state = state
        self._service._message_text = message_text
        self._service._telegram_user = TelegramUserDTOModel(**self._response_data["detail"])

        mock_work_with_message_text = AsyncMock(return_value=state)
        self._service._work_with_message_text = mock_work_with_message_text
        mock_work_with_start_learn_words_status = AsyncMock(return_value=state)
        self._service._work_with_start_learn_words_status = mock_work_with_start_learn_words_status
        mock_work_with_read_status = AsyncMock(return_value=state)
        self._service.work_with_read_status = mock_work_with_read_status

        await self._service.get_real_state()

        mock_work_with_message_text.assert_not_called()
        mock_work_with_start_learn_words_status.assert_not_called()
        mock_work_with_read_status.assert_called_once()

    @mark.parametrize(
        "message_text, state, expected_state, is_update",
        [
            ("/profile", State.read_book.value, State.update_profile.value, True),
            (
                "/profile",
                State.check_answer_time.value,
                State.update_profile.value,
                True,
            ),
            ("/profile", State.check_answer_time.value, State.error.value, False),
            ("/profile", State.read_book.value, State.error.value, False),
        ],
    )
    @mark.asyncio
    async def test_work_with_message_text_profile(self, message_text, state, expected_state, is_update):
        self._service._state = state
        self._service._message_text = message_text
        self._service._telegram_user = TelegramUserDTOModel(**self._response_data["detail"])

        mock_update_state = AsyncMock(return_value=is_update)
        self._service._update_state = mock_update_state

        await self._service._work_with_message_text()
        mock_update_state.assert_called_once()
        assert self._service._state == expected_state

    @mark.parametrize(
        "message_text, state, expected_state",
        [
            ("/records", State.read_book.value, State.records.value),
            ("/records", State.check_answer_time.value, State.records.value),
            ("/achievements", State.check_answer_time.value, State.achievements.value),
            ("/achievements", State.read_book.value, State.achievements.value),
        ],
    )
    @mark.asyncio
    async def test_work_with_message_text_other(self, message_text, state, expected_state):
        self._service._state = state
        self._service._message_text = message_text
        self._service._telegram_user = TelegramUserDTOModel(**self._response_data["detail"])

        mock_update_state = AsyncMock(return_value=True)
        self._service._update_state = mock_update_state

        await self._service._work_with_message_text()
        mock_update_state.assert_not_called()
        assert self._service._state == expected_state

    @mark.parametrize(
        "state, expected_is_update",
        [
            (State.read_book.value, True),
            (State.check_answer_time.value, True),
            (State.learn_words.value, True),
            (State.start_learn_words.value, True),
            (State.check_answer_time.value, False),
            (State.read_book.value, False),
        ],
    )
    @patch("middlewears.set_state.update_data_by_api")
    @mark.asyncio
    async def test_update_state(self, mock_update_data_by_api, state, expected_is_update):
        mock_update_data_by_api.return_value = expected_is_update
        self._service._state = state
        self._service._telegram_user = TelegramUserDTOModel(**self._response_data["detail"])
        self._service._telegram_user.stage = state

        is_update = await self._service._update_state()

        if state in {State.read_book.value, State.check_answer_time.value}:
            mock_update_data_by_api.assert_called_once_with(
                telegram_id=self._service._telegram_user.telegram_id,
                params_for_update={
                    "telegram_id": self._service._telegram_user.telegram_id,
                    "previous_stage": state,
                },
                url_for_update=f"telegram_user/{self._service._telegram_user.telegram_id}",
            )
        else:
            mock_update_data_by_api.assert_not_called()

        assert is_update == expected_is_update

    @mark.asyncio
    async def test_work_with_read_status(self, sentence_with_word):
        self._service._telegram_user = TelegramUserDTOModel(**self._response_data["detail"])

        self._service._state = State.check_answer_time.value

        # Проверяем без предложения
        mock_get_new_sentence = AsyncMock(return_value="state")
        self._service._get_new_sentence = mock_get_new_sentence
        return_value = await self._service.work_with_read_status()
        mock_get_new_sentence.assert_called_once()
        assert return_value == "state"
        # Проверяем с предложением
        mock_get_new_sentence = AsyncMock(return_value="state")
        self._service._get_new_sentence = mock_get_new_sentence
        self._service._telegram_user.new_sentence = sentence_with_word
        return_value = await self._service.work_with_read_status()
        mock_get_new_sentence.assert_not_called()
        assert return_value == State.check_answer_time.value
        # Проверяем для другого state и со словами
        self._service._state = State.read_book.value
        assert self._service._telegram_user.new_sentence.words
        self._service._get_new_sentence = mock_get_new_sentence
        self._service._telegram_user.new_sentence = sentence_with_word
        return_value = await self._service.work_with_read_status()
        mock_get_new_sentence.assert_not_called()
        assert return_value == State.check_words.value
        # Проверяем для предложения без слов, но с текстом
        self._service._state = State.read_book.value
        self._service._telegram_user.new_sentence.words = []
        self._service._get_new_sentence = mock_get_new_sentence
        self._service._telegram_user.new_sentence = sentence_with_word
        return_value = await self._service.work_with_read_status()
        mock_get_new_sentence.assert_not_called()
        assert return_value == State.read_book.value
        # Проверяем для предложения без слов, и без текста
        self._service._state = State.read_book.value
        self._service._telegram_user.new_sentence.text = ""
        self._service._get_new_sentence = mock_get_new_sentence
        self._service._telegram_user.new_sentence = sentence_with_word
        return_value = await self._service.work_with_read_status()
        mock_get_new_sentence.assert_called_once()
        assert return_value == "state"

    @mark.parametrize(
        "response_status, count_words",
        [
            (HTTPStatus.OK, 1),
            (HTTPStatus.BAD_REQUEST, 1),
            (HTTPStatus.OK, 0),
        ],
    )
    @mark.asyncio
    async def test_work_with_start_learn_words_status(self, response_status, count_words):
        self._service._telegram_user = TelegramUserDTOModel(**self._response_data["detail"])
        self._service._telegram_user.learn_words = []
        mock_work_with_read_status = AsyncMock(return_value="state")
        self._service.work_with_read_status = mock_work_with_read_status
        word = {
            "word_id": 1,
            "word": "test",
            "type_word_id": 1,
            "transcription": "test",
            "part_of_speech": "n",
            "is_known": True,
            "count_view": 0,
            "correct_answers": 0,
            "incorrect_answers": 0,
            "correct_answers_in_row": 0,
            "increase_factor": 0,
            "interval_repeat": 0,
            "repeat_datetime": datetime.now(),
        }
        response_data = [word for _ in range(count_words)]
        expected_learn_words = [WordDTOModel(**word) for _ in range(count_words)]
        with patch(self._get_method_target, return_value=(response_data, response_status)) as mocked_get:
            state = await self._service._work_with_start_learn_words_status()

        mocked_get.assert_called_once_with(
            url=f"{settings.api_url}/v1/history/learn-words/{self._chat}/",
            headers=settings.api_headers,
        )

        if response_status == HTTPStatus.OK and count_words > 0:
            assert self._service._telegram_user.learn_words == expected_learn_words
            assert state == State.start_learn_words.value
        elif response_status == HTTPStatus.OK:
            mock_work_with_read_status.assert_called_once()
            assert self._service._telegram_user.learn_words == []
            assert self._service._state == State.read_book.value
            assert state == "state"
        else:
            assert self._service._telegram_user.learn_words == []
            assert state == State.error.value

    @mark.parametrize(
        "response_status, stage, expected_stage, is_words",
        [
            (
                HTTPStatus.PARTIAL_CONTENT,
                State.check_answer_time.value,
                State.check_answer_time.value,
                True,
            ),
            (
                HTTPStatus.PARTIAL_CONTENT,
                State.read_book.value,
                State.read_book_end.value,
                True,
            ),
            (HTTPStatus.BAD_REQUEST, State.read_book.value, State.error.value, True),
            (HTTPStatus.OK, State.read_book.value, State.check_words.value, True),
            (
                HTTPStatus.OK,
                State.check_answer_time.value,
                State.check_answer_time.value,
                True,
            ),
            (HTTPStatus.OK, State.read_book.value, State.read_book.value, False),
        ],
    )
    @mark.asyncio
    async def test_get_new_sentence(self, sentence_with_word, response_status, stage, expected_stage, is_words):
        self._service._telegram_user = TelegramUserDTOModel(**self._response_data["detail"])
        self._service._state = stage

        sentence = sentence_with_word.dict()
        if is_words is False:
            sentence["words"] = []
        response_data = {"detail": sentence}
        with patch(self._get_method_target, return_value=(response_data, response_status)) as mocked_get:
            state = await self._service._get_new_sentence()

        mocked_get.assert_called_once_with(
            url=f"{settings.api_url}/v1/read/{self._chat}/",
            headers=settings.api_headers,
        )

        assert state == expected_stage
