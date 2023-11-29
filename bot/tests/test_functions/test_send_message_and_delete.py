from unittest.mock import AsyncMock, patch

from aiogram.utils.exceptions import MessageCantBeDeleted
from pytest import mark

from functions import delete_message, send_message_and_delete


class TestSendDeleteMessageFunction:
    """Tests for delete and send message function."""

    @patch('functions.send_and_delete_message.bot', new_callable=AsyncMock)
    @mark.asyncio
    async def test_delete_message(self, mock_bot):
        mock_bot.side_effect = [MessageCantBeDeleted]
        await delete_message(chat_id=1, message_id=1)
        mock_bot.delete_message.assert_called_once_with(chat_id=1, message_id=1)
