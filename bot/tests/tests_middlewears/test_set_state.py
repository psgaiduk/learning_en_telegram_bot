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

    @pytest.mark.asyncio
    async def test_get_state_registration(self, mocker):

        message = Mock(from_user=Mock(id=self._user), chat=Mock(id=self._chat), spec=types.Message)
        storage_mock = Mock(spec=BaseStorage)
        dispatcher_mock = Mock(storage=storage_mock)
        service = SetStateMiddleware(dispatcher_mock)
        response_mock = mocker.AsyncMock(spec=ClientResponse)
        response_mock.status = HTTPStatus.NOT_FOUND

        storage_mock.check_address.return_value = (self._chat, self._user)

        fsm_context_mock = mocker.Mock(spec=FSMContext)

        fsm_context_mock.set_state = mocker.AsyncMock()

        fsm_context_constructor_mock = mocker.patch('middlewears.set_state.FSMContext', return_value=fsm_context_mock)

        with patch(self._get_method_target, return_value=response_mock) as mocked_get:
            await service.on_pre_process_message(message=message, data={})

        mocked_get.assert_called_once_with(
            url=f'{settings.api_url}/v1/telegram_user/{self._chat}',
            headers=settings.api_headers,
        )

        fsm_context_constructor_mock.assert_called()
        fsm_context_constructor_mock.assert_called_once_with(storage=storage_mock, chat=self._chat, user=self._user)
        expected_state = 'REGISTRATION'
        fsm_context_mock.set_state.assert_called_once_with(state=expected_state)

    @pytest.mark.asyncio
    async def test_get_state_from_user(self, mocker):
        message = Mock(from_user=Mock(id=self._user), chat=Mock(id=self._chat), spec=types.Message)
        storage_mock = Mock(spec=BaseStorage)
        dispatcher_mock = Mock(storage=storage_mock)
        service = SetStateMiddleware(dispatcher_mock)
        response_mock = mocker.AsyncMock(spec=ClientResponse)
        response_mock.status = HTTPStatus.OK
        response_mock.json = mocker.AsyncMock(return_value={'detail': {'stage': 'WAIT_NAME'}})
        storage_mock.check_address.return_value = (self._chat, self._user)

        fsm_context_mock = mocker.Mock(spec=FSMContext)
        fsm_context_mock.set_state = mocker.AsyncMock()
        fsm_context_constructor_mock = mocker.patch('middlewears.set_state.FSMContext', return_value=fsm_context_mock)

        with patch(self._get_method_target, return_value=response_mock) as mocked_get:
            await service.on_pre_process_message(message=message, data={})

        mocked_get.assert_called_once_with(
            url=f'{settings.api_url}/v1/telegram_user/{self._chat}',
            headers=settings.api_headers,
        )

        fsm_context_constructor_mock.assert_called()
        fsm_context_constructor_mock.assert_called_once_with(storage=storage_mock, chat=self._chat, user=self._user)
        expected_state = 'WAIT_NAME'
        fsm_context_mock.set_state.assert_called_once_with(state=expected_state)


