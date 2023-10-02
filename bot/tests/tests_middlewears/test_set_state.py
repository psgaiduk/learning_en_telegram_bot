import pytest

from aiogram import types
from aiogram.dispatcher.storage import BaseStorage, FSMContext
from aiohttp import ClientResponse
from http import HTTPStatus
from unittest.mock import Mock, patch

from middlewears import SetStateMiddleware
from settings import settings


class TestSetStateMiddleware:
    """Tests for SetStateMiddleware."""

    @classmethod
    def setup_class(cls):
        cls._chat = 12345
        cls._user = 12345
        cls._message = Mock()
        cls._get_method_target = 'context_managers.aio_http_client.AsyncHttpClient.get'
        cls._storage_mock = Mock(spec=BaseStorage)
        cls._service = SetStateMiddleware(dispatcher=Mock(storage=cls._storage_mock))

    @pytest.mark.asyncio
    async def test_get_state_registration(self, mocker):

        message = Mock(from_user=Mock(id=self._user), chat=Mock(id=self._chat), spec=types.Message)
        response_mock = mocker.AsyncMock(spec=ClientResponse)
        response_mock.status = HTTPStatus.NOT_FOUND

        self._storage_mock.check_address.return_value = (self._chat, self._user)

        fsm_context_mock = mocker.Mock(spec=FSMContext)
        fsm_context_mock.set_state = mocker.AsyncMock()
        fsm_context_constructor_mock = mocker.patch('middlewears.set_state.FSMContext', return_value=fsm_context_mock)

        with patch(self._get_method_target, return_value=response_mock) as mocked_get:
            await self._service.on_pre_process_message(message=message, data={})

        mocked_get.assert_called_once_with(
            url=f'{settings.api_url}/v1/telegram_user/{self._chat}',
            headers=settings.api_headers,
        )

        fsm_context_constructor_mock.assert_called()
        fsm_context_constructor_mock.assert_called_once_with(storage=self._storage_mock, chat=self._chat, user=self._user)
        expected_state = 'REGISTRATION'
        fsm_context_mock.set_state.assert_called_once_with(state=expected_state)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'stage',
        [('WAIT_NAME',), ('WAIT_EN_LEVEL',), ('READ_BOOK',), ('CHECK_WORDS',), ('GRAMMAR',), ('UPDATE_PROFILE',)],
    )
    async def test_get_state_from_user(self, mocker, stage):
        message = Mock(from_user=Mock(id=self._user), chat=Mock(id=self._chat), spec=types.Message)
        response_mock = mocker.AsyncMock(spec=ClientResponse)
        response_mock.status = HTTPStatus.OK
        response_mock.json = mocker.AsyncMock(return_value={'detail': {'stage': stage}})

        self._storage_mock.check_address.return_value = (self._chat, self._user)

        fsm_context_mock = mocker.Mock(spec=FSMContext)
        fsm_context_mock.set_state = mocker.AsyncMock()
        fsm_context_constructor_mock = mocker.patch('middlewears.set_state.FSMContext', return_value=fsm_context_mock)

        with patch(self._get_method_target, return_value=response_mock) as mocked_get:
            await self._service.on_pre_process_message(message=message, data={})

        mocked_get.assert_called_once_with(
            url=f'{settings.api_url}/v1/telegram_user/{self._chat}',
            headers=settings.api_headers,
        )

        fsm_context_constructor_mock.assert_called()
        fsm_context_constructor_mock.assert_called_once_with(storage=self._storage_mock, chat=self._chat, user=self._user)
        expected_state = stage
        fsm_context_mock.set_state.assert_called_once_with(state=expected_state)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('stage', [('WAIT_NAME',), ('WAIT_EN_LEVEL',), ('READ_BOOK',)])
    async def test_get_state_update_profile(self, mocker, stage):
        message = Mock(from_user=Mock(id=self._user), chat=Mock(id=self._chat), text='/profile', spec=types.Message)
        response_mock = mocker.AsyncMock(spec=ClientResponse)
        response_mock.status = HTTPStatus.OK
        response_mock.json = mocker.AsyncMock(return_value={'detail': {'stage': stage}})

        self._storage_mock.check_address.return_value = (self._chat, self._user)

        fsm_context_mock = mocker.Mock(spec=FSMContext)
        fsm_context_mock.set_state = mocker.AsyncMock()
        fsm_context_constructor_mock = mocker.patch('middlewears.set_state.FSMContext', return_value=fsm_context_mock)

        with patch(self._get_method_target, return_value=response_mock) as mocked_get:
            await self._service.on_pre_process_message(message=message, data={})

        mocked_get.assert_called_once_with(
            url=f'{settings.api_url}/v1/telegram_user/{self._chat}',
            headers=settings.api_headers,
        )

        fsm_context_constructor_mock.assert_called()
        fsm_context_constructor_mock.assert_called_once_with(storage=self._storage_mock, chat=self._chat, user=self._user)
        expected_state = 'UPDATE_PROFILE'
        fsm_context_mock.set_state.assert_called_once_with(state=expected_state)


