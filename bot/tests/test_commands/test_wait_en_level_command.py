from unittest.mock import AsyncMock, Mock, patch

from pytest import mark

from bot import bot
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

    @mark.asyncio
    async def test_handle_wait_en_level_other_data(self):
        chat_id = 1
        callback = Mock()
        callback.data = 'test'
        callback.from_user.id = chat_id

        with patch.object(bot, 'send_message', new=AsyncMock()) as mock_send_message:

            await handle_wait_en_level_incorrect_text(message=callback)

            mock_send_message.assert_called_once_with(
                chat_id=chat_id,
                text='Нужно нажать по одной из кнопок, чтобы изменить уровень английского.',
            )
