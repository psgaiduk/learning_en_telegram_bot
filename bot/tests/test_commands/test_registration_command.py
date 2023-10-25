from unittest.mock import AsyncMock, MagicMock, patch

from aiogram import types
from pytest import mark

from commands import handle_registration


class TestRegistrationCommand:
    """Tests command registration."""

    @patch('commands.registration.RegistrationService')
    @mark.asyncio
    async def test_handle_registration(self, mock_registration_service, monkeypatch):
        monkeypatch.setattr('commands.registration.State', MagicMock(value='registration'))
        mock_message = types.Message(message_id=1, chat=types.Chat(id=1), text='/start')

        mock_registration_service.return_value.do = AsyncMock()

        await handle_registration(mock_message)

        mock_registration_service.assert_called_once_with(message=mock_message)
        mock_registration_service.return_value.do.assert_called_once()
