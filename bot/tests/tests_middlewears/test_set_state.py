import pytest

from aiogram import types
from aiogram.dispatcher.storage import BaseStorage, FSMContext
from http import HTTPStatus
from unittest.mock import AsyncMock, Mock, patch

from choices import State
from dto import TelegramUserDTOModel, NewSentenceDTOModel, WordDTOModel
from middlewears import SetStateMiddleware
from settings import settings


class TestSetStateMiddleware:
    """Tests for SetStateMiddleware."""

    def setup_method(self):
        self._chat = 12345
        self._user = 12345
        self._message = Mock()
        self._get_method_target = 'context_managers.aio_http_client.AsyncHttpClient.get'
        self._storage_mock = Mock(spec=BaseStorage)
        self._service = SetStateMiddleware(dispatcher=Mock(storage=self._storage_mock))
        self._response_data = {
            'detail': {
                'stage': '',
                'user_name': 'test_name',
                'experience': 0,
                'previous_stage': '',
                'telegram_id': 12345,
                'hero_level': None,
                'level_en': None,
                'main_language': None,
            }
        }
        self._new_sentence = NewSentenceDTOModel(
            history_sentence_id=1,
            book_id=1,
            sentence_id=1,
            text='test_text',
            translation={'ru': 'test_text'},
            words=[
                WordDTOModel(
                    word_id=1,
                    word='test_word',
                    type_word_id=1,
                    translation={'ru': 'test_word'},
                    is_known=False,
                    count_view=0,
                    correct_answers=0,
                    incorrect_answers=0,
                    correct_answers_in_row=0,
                )
            ],
        )

    # @pytest.mark.asyncio
    # async def test_get_state_registration(self, mocker):
    #
    #     message = Mock(from_user=Mock(id=self._user), chat=Mock(id=self._chat), spec=types.Message)
    #
    #     self._storage_mock.check_address.return_value = (self._chat, self._user)
    #
    #     fsm_context_mock = mocker.Mock(spec=FSMContext)
    #     fsm_context_mock.set_state = mocker.AsyncMock()
    #     fsm_context_constructor_mock = mocker.patch('middlewears.set_state.FSMContext', return_value=fsm_context_mock)
    #
    #     with patch(self._get_method_target, return_value=({}, HTTPStatus.NOT_FOUND)) as mocked_get:
    #         await self._service.on_pre_process_message(message=message, data={})
    #
    #     mocked_get.assert_called_once_with(
    #         url=f'{settings.api_url}/v1/telegram_user/{self._chat}',
    #         headers=settings.api_headers,
    #     )
    #
    #     fsm_context_constructor_mock.assert_called()
    #     fsm_context_constructor_mock.assert_called_once_with(storage=self._storage_mock, chat=self._chat, user=self._user)
    #     expected_state = 'REGISTRATION'
    #     fsm_context_mock.set_state.assert_called_once_with(state=expected_state)
    #
    # @pytest.mark.asyncio
    # @pytest.mark.parametrize(
    #     'stage',
    #     ['WAIT_NAME', 'WAIT_EN_LEVEL', 'GRAMMAR', 'UPDATE_PROFILE'],
    # )
    # async def test_get_state_from_user(self, mocker, stage):
    #     message = Mock(from_user=Mock(id=self._user), chat=Mock(id=self._chat), spec=types.Message)
    #     response_data = self._response_data
    #     response_data['detail']['stage'] = stage
    #
    #     self._storage_mock.check_address.return_value = (self._chat, self._user)
    #
    #     fsm_context_mock = mocker.Mock(spec=FSMContext)
    #     fsm_context_mock.set_state = mocker.AsyncMock()
    #     fsm_context_constructor_mock = mocker.patch('middlewears.set_state.FSMContext', return_value=fsm_context_mock)
    #
    #     with patch(self._get_method_target, return_value=(response_data, HTTPStatus.OK)) as mocked_get:
    #         await self._service.on_pre_process_message(message=message, data={})
    #
    #     mocked_get.assert_called_once_with(
    #         url=f'{settings.api_url}/v1/telegram_user/{self._chat}',
    #         headers=settings.api_headers,
    #     )
    #
    #     fsm_context_constructor_mock.assert_called()
    #     fsm_context_constructor_mock.assert_called_once_with(storage=self._storage_mock, chat=self._chat, user=self._user)
    #     expected_state = stage
    #     fsm_context_mock.set_state.assert_called_once_with(state=expected_state)
    #
    #     telegram_user = TelegramUserDTOModel(**response_data['detail'])
    #
    #     expected_data = {'user': telegram_user}
    #     fsm_context_mock.set_data.assert_called_once_with(data=expected_data)
    #
    # @pytest.mark.parametrize('stage', ['WAIT_NAME', 'WAIT_EN_LEVEL', 'READ_BOOK'])
    # @patch('middlewears.set_state.update_data_by_api', new_callable=AsyncMock)
    # @pytest.mark.asyncio
    # async def test_get_state_update_profile(self, mock_update_user, mocker, stage):
    #     message = Mock(from_user=Mock(id=self._user), chat=Mock(id=self._chat), text='/profile', spec=types.Message)
    #     response_data = self._response_data
    #     response_data['detail']['stage'] = stage
    #     mock_update_user.side_effect = [True]
    #
    #     self._storage_mock.check_address.return_value = (self._chat, self._user)
    #
    #     fsm_context_mock = mocker.Mock(spec=FSMContext)
    #     fsm_context_mock.set_state = mocker.AsyncMock()
    #     fsm_context_constructor_mock = mocker.patch('middlewears.set_state.FSMContext', return_value=fsm_context_mock)
    #
    #     with patch(self._get_method_target, return_value=(response_data, HTTPStatus.OK)) as mocked_get:
    #         await self._service.on_pre_process_message(message=message, data={})
    #
    #     mocked_get.assert_called_once_with(
    #         url=f'{settings.api_url}/v1/telegram_user/{self._chat}',
    #         headers=settings.api_headers,
    #     )
    #
    #     fsm_context_constructor_mock.assert_called()
    #     fsm_context_constructor_mock.assert_called_once_with(storage=self._storage_mock, chat=self._chat, user=self._user)
    #     expected_state = 'UPDATE_PROFILE'
    #     fsm_context_mock.set_state.assert_called_once_with(state=expected_state)
    #
    #     if stage == 'READ_BOOK':
    #         expected_data_for_update_user = {
    #             'telegram_id': self._chat,
    #             'previous_stage': State.read_book.value,
    #         }
    #
    #         mock_update_user.assert_awaited_once_with(
    #             telegram_id=self._chat,
    #             params_for_update=expected_data_for_update_user,
    #             url_for_update=f'telegram_user/{self._chat}',
    #         )
    #     else:
    #         mock_update_user.assert_not_called()
    #
    # @pytest.mark.asyncio
    # @pytest.mark.parametrize('stage', ['GRAMMAR'])
    # async def test_not_get_state_update_profile(self, mocker, stage):
    #     message = Mock(from_user=Mock(id=self._user), chat=Mock(id=self._chat), text='/profile', spec=types.Message)
    #     response_data = self._response_data
    #     response_data['detail']['stage'] = stage
    #
    #     self._storage_mock.check_address.return_value = (self._chat, self._user)
    #
    #     fsm_context_mock = mocker.Mock(spec=FSMContext)
    #     fsm_context_mock.set_state = mocker.AsyncMock()
    #     fsm_context_constructor_mock = mocker.patch('middlewears.set_state.FSMContext', return_value=fsm_context_mock)
    #
    #     with patch(self._get_method_target, return_value=(response_data, HTTPStatus.OK)) as mocked_get:
    #         await self._service.on_pre_process_message(message=message, data={})
    #
    #     mocked_get.assert_called_once_with(
    #         url=f'{settings.api_url}/v1/telegram_user/{self._chat}',
    #         headers=settings.api_headers,
    #     )
    #
    #     fsm_context_constructor_mock.assert_called()
    #     fsm_context_constructor_mock.assert_called_once_with(storage=self._storage_mock, chat=self._chat, user=self._user)
    #     expected_state = stage
    #     fsm_context_mock.set_state.assert_called_once_with(state=expected_state)
    #
    # @pytest.mark.asyncio
    # @pytest.mark.parametrize('stage', ['WAIT_NAME', 'WAIT_EN_LEVEL', 'READ_BOOK'])
    # async def test_get_state_records(self, mocker, stage):
    #     message = Mock(from_user=Mock(id=self._user), chat=Mock(id=self._chat), text='/records', spec=types.Message)
    #     response_data = self._response_data
    #     response_data['detail']['stage'] = stage
    #
    #     self._storage_mock.check_address.return_value = (self._chat, self._user)
    #
    #     fsm_context_mock = mocker.Mock(spec=FSMContext)
    #     fsm_context_mock.set_state = mocker.AsyncMock()
    #     fsm_context_constructor_mock = mocker.patch('middlewears.set_state.FSMContext', return_value=fsm_context_mock)
    #
    #     with patch(self._get_method_target, return_value=(response_data, HTTPStatus.OK)) as mocked_get:
    #         await self._service.on_pre_process_message(message=message, data={})
    #
    #     mocked_get.assert_called_once_with(
    #         url=f'{settings.api_url}/v1/telegram_user/{self._chat}',
    #         headers=settings.api_headers,
    #     )
    #
    #     fsm_context_constructor_mock.assert_called()
    #     fsm_context_constructor_mock.assert_called_once_with(storage=self._storage_mock, chat=self._chat, user=self._user)
    #     expected_state = 'RECORDS'
    #     fsm_context_mock.set_state.assert_called_once_with(state=expected_state)
    #
    # @pytest.mark.asyncio
    # @pytest.mark.parametrize('stage', ['GRAMMAR', 'UPDATE_PROFILE'])
    # async def test_not_get_state_records(self, mocker, stage):
    #     message = Mock(from_user=Mock(id=self._user), chat=Mock(id=self._chat), text='/records', spec=types.Message)
    #     response_data = self._response_data
    #     response_data['detail']['stage'] = stage
    #
    #     self._storage_mock.check_address.return_value = (self._chat, self._user)
    #
    #     fsm_context_mock = mocker.Mock(spec=FSMContext)
    #     fsm_context_mock.set_state = mocker.AsyncMock()
    #     fsm_context_constructor_mock = mocker.patch('middlewears.set_state.FSMContext', return_value=fsm_context_mock)
    #
    #     with patch(self._get_method_target, return_value=(response_data, HTTPStatus.OK)) as mocked_get:
    #         await self._service.on_pre_process_message(message=message, data={})
    #
    #     mocked_get.assert_called_once_with(
    #         url=f'{settings.api_url}/v1/telegram_user/{self._chat}',
    #         headers=settings.api_headers,
    #     )
    #
    #     fsm_context_constructor_mock.assert_called()
    #     fsm_context_constructor_mock.assert_called_once_with(storage=self._storage_mock, chat=self._chat, user=self._user)
    #     expected_state = stage
    #     fsm_context_mock.set_state.assert_called_once_with(state=expected_state)
    #
    # @pytest.mark.asyncio
    # @pytest.mark.parametrize('stage', ['WAIT_NAME', 'WAIT_EN_LEVEL', 'READ_BOOK'])
    # async def test_get_state_achievements(self, mocker, stage):
    #     message = Mock(from_user=Mock(id=self._user), chat=Mock(id=self._chat), text='/achievements', spec=types.Message)
    #     response_data = self._response_data
    #     response_data['detail']['stage'] = stage
    #
    #     self._storage_mock.check_address.return_value = (self._chat, self._user)
    #
    #     fsm_context_mock = mocker.Mock(spec=FSMContext)
    #     fsm_context_mock.set_state = mocker.AsyncMock()
    #     fsm_context_constructor_mock = mocker.patch('middlewears.set_state.FSMContext', return_value=fsm_context_mock)
    #
    #     with patch(self._get_method_target, return_value=(response_data, HTTPStatus.OK)) as mocked_get:
    #         await self._service.on_pre_process_message(message=message, data={})
    #
    #     mocked_get.assert_called_once_with(
    #         url=f'{settings.api_url}/v1/telegram_user/{self._chat}',
    #         headers=settings.api_headers,
    #     )
    #
    #     fsm_context_constructor_mock.assert_called()
    #     fsm_context_constructor_mock.assert_called_once_with(storage=self._storage_mock, chat=self._chat, user=self._user)
    #     expected_state = 'ACHIEVEMENTS'
    #     fsm_context_mock.set_state.assert_called_once_with(state=expected_state)
    #
    # @pytest.mark.asyncio
    # @pytest.mark.parametrize('stage', ['GRAMMAR', 'UPDATE_PROFILE'])
    # async def test_not_get_state_achievements(self, mocker, stage):
    #     message = Mock(from_user=Mock(id=self._user), chat=Mock(id=self._chat), text='/achievements', spec=types.Message)
    #     response_data = self._response_data
    #     response_data['detail']['stage'] = stage
    #
    #     self._storage_mock.check_address.return_value = (self._chat, self._user)
    #
    #     fsm_context_mock = mocker.Mock(spec=FSMContext)
    #     fsm_context_mock.set_state = mocker.AsyncMock()
    #     fsm_context_constructor_mock = mocker.patch('middlewears.set_state.FSMContext', return_value=fsm_context_mock)
    #
    #     with patch(self._get_method_target, return_value=(response_data, HTTPStatus.OK)) as mocked_get:
    #         await self._service.on_pre_process_message(message=message, data={})
    #
    #     mocked_get.assert_called_once_with(
    #         url=f'{settings.api_url}/v1/telegram_user/{self._chat}',
    #         headers=settings.api_headers,
    #     )
    #
    #     fsm_context_constructor_mock.assert_called()
    #     fsm_context_constructor_mock.assert_called_once_with(storage=self._storage_mock, chat=self._chat, user=self._user)
    #     expected_state = stage
    #     fsm_context_mock.set_state.assert_called_once_with(state=expected_state)

    @pytest.mark.parametrize('response_status, expected_state', [
        (HTTPStatus.NOT_FOUND, State.registration.value),
        (HTTPStatus.OK, 'expected_stage_from_api'),
        (HTTPStatus.BAD_REQUEST, State.error.value),
    ])
    @pytest.mark.asyncio
    async def test_set_state_data(self, mocker, response_status, expected_state):
        response_data = self._response_data
        response_data['detail']['stage'] = expected_state

        self._storage_mock.check_address.return_value = (self._chat, self._user)

        fsm_context_mock = mocker.Mock(spec=FSMContext)
        fsm_context_mock.set_state = mocker.AsyncMock()
        mocker.patch('middlewears.set_state.FSMContext', return_value=fsm_context_mock)

        mock_get_real_state = AsyncMock(return_value=expected_state)
        self._service.get_real_state = mock_get_real_state

        with patch(self._get_method_target, return_value=(response_data, response_status)) as mocked_get:
            await self._service.set_state_data(user=self._chat, telegram_id=self._chat)

        mocked_get.assert_called_once_with(
            url=f'{settings.api_url}/v1/telegram_user/{self._chat}',
            headers=settings.api_headers,
        )

        fsm_context_mock.set_state.assert_called_once_with(state=expected_state)

        if response_status == HTTPStatus.OK:
            assert self._service._telegram_user == TelegramUserDTOModel(**response_data['detail'])
            expected_data = {'user': TelegramUserDTOModel(**response_data['detail'])}
            fsm_context_mock.set_data.assert_called_once_with(data=expected_data)
        else:
            fsm_context_mock.set_data.assert_not_called()
            assert self._service._telegram_user is None

    @pytest.mark.parametrize('state', [State.update_profile.value, State.error.value, State.grammar.value, State.registration.value])
    @patch('middlewears.set_state.update_data_by_api', new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_get_real_state_regular_work(self, mock_update_user, state):
        self._service._state = state
        self._service._message_text = 'text'
        mock_update_user.side_effect = [True]
        mock_work_with_read_status = AsyncMock(return_value=state)
        self._service.work_with_read_status = mock_work_with_read_status

        assert await self._service.get_real_state() == state

        mock_update_user.assert_not_called()
        mock_work_with_read_status.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_real_test_read_book(self):
        state = State.read_book.value
        self._service._state = state
        self._service._message_text = 'text'

        mock_work_with_read_status = AsyncMock(return_value=state)
        self._service.work_with_read_status = mock_work_with_read_status

        assert await self._service.get_real_state() == state
        mock_work_with_read_status.assert_called_once()

    @pytest.mark.parametrize('message_text, state, expected_state, is_update', [
        ('/profile', State.registration.value, State.registration.value, None),
        ('/profile', State.error.value, State.error.value, None),
        ('/profile', State.grammar.value, State.grammar.value, None),
        ('/profile', State.read_book.value, State.update_profile.value, True),
        ('/profile', State.read_book.value, State.error.value, False),
        ('/profile', State.wait_name.value, State.update_profile.value, None),
        ('/profile', State.wait_en_level.value, State.update_profile.value, None),
        ('/records', State.registration.value, State.registration.value, None),
        ('/records', State.error.value, State.error.value, None),
        ('/records', State.grammar.value, State.grammar.value, None),
        ('/records', State.update_profile.value, State.update_profile.value, None),
        ('/records', State.read_book.value, State.records.value, None),
        ('/achievements', State.registration.value, State.registration.value, None),
        ('/achievements', State.error.value, State.error.value, None),
        ('/achievements', State.grammar.value, State.grammar.value, None),
        ('/achievements', State.update_profile.value, State.update_profile.value, None),
        ('/achievements', State.read_book.value, State.achievements.value, None),
        ('just text', State.update_profile.value, State.update_profile.value, None),
        ('just text', State.read_book.value, State.read_book.value, None),
    ])
    @patch('middlewears.set_state.update_data_by_api', new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_get_real_state_regular_work(self, mock_update_user, message_text, state, expected_state, is_update):
        self._service._state = state
        self._service._message_text = message_text
        self._service._telegram_user = TelegramUserDTOModel(**self._response_data['detail'])
        self._service._telegram_user.stage = state
        mock_update_user.side_effect = [is_update]

        mock_work_with_read_status = AsyncMock(return_value=state)

        if state == State.read_book.value and message_text not in {'/profile', '/records', '/achievements'}:
            self._service.work_with_read_status = mock_work_with_read_status
        else:
            self._service.work_with_read_status = mock_work_with_read_status

        assert await self._service.get_real_state() == expected_state
        
        if message_text == '/profile' and state == State.read_book.value:
            expected_data_for_update_user = {
                'telegram_id': self._service._telegram_user.telegram_id,
                'previous_stage': self._service._telegram_user.stage,
            }

            mock_update_user.assert_awaited_once_with(
                telegram_id=self._service._telegram_user.telegram_id,
                params_for_update=expected_data_for_update_user,
                url_for_update=f'telegram_user/{self._service._telegram_user.telegram_id}',
            )
        else:
            mock_update_user.assert_not_called()

    @pytest.mark.parametrize('response_status, words, expected_state', [
        (HTTPStatus.OK, [], State.read_book.value),
        (HTTPStatus.OK, ['word'], State.check_words.value),
        (HTTPStatus.BAD_REQUEST, ['word'], State.error.value),
    ])
    @pytest.mark.asyncio
    async def test_work_with_read_status(self, response_status, words, expected_state):
        response_data = {'detail': self._new_sentence.dict()}
        self._service._telegram_user = TelegramUserDTOModel(**self._response_data['detail'])
        self._service._telegram_user.stage = 'READ_BOOK'
        if not words:
            response_data['detail']['words'] = []

        with patch(self._get_method_target, return_value=(response_data, response_status)) as mocked_get:
            updated_state = await self._service.work_with_read_status()

        mocked_get.assert_called_once_with(
            url=f'{settings.api_url}/v1/read/{self._chat}/',
            headers=settings.api_headers,
        )

        assert updated_state == expected_state
        if updated_state != State.error.value:
            assert self._service._telegram_user.new_sentence == NewSentenceDTOModel(**response_data['detail'])
        else:
            assert self._service._telegram_user.new_sentence is None
