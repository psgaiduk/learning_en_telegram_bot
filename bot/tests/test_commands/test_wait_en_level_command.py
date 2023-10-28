from unittest.mock import AsyncMock, Mock, patch

from pytest import mark

from bot import bot
from choices import State
from commands import (
    handle_wait_en_level,
    handle_wait_en_level_incorrect_text,
)


class TestWaitEnLevelCommand:
    """Tests command wait english level."""

    @patch('commands.wait_en_level.WaitEnLevelService')
    @mark.asyncio
    async def test_handle_wait_en_level(self, mock_wait_en_level_service):
        chat_id = 1
        callback = Mock()
        callback.data = 'user_profile_'
        callback.from_user.id = chat_id
        state = Mock()

        mock_wait_en_level_service.return_value.do = AsyncMock()

        await handle_wait_en_level(callback_query=callback, state=state)

        mock_wait_en_level_service.assert_called_once_with(callback_query=callback, state=state)
        mock_wait_en_level_service.return_value.do.assert_called_once()
