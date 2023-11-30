from unittest.mock import AsyncMock, patch

from aiogram.utils.exceptions import MessageCantBeDeleted
from pytest import mark

from functions import delete_message, send_message_and_delete


class TestSendDeleteMessageFunction:
    """Tests for delete and send message function."""

    @mark.parametrize('error, is_delete', [(None, True), (MessageCantBeDeleted, True), (ValueError, False), (AttributeError, True)])
    @patch('functions.send_and_delete_message.bot', new_callable=AsyncMock)
    @mark.asyncio
    async def test_delete_message(self, mock_bot, error, is_delete):
        mock_bot.delete_message.side_effect = error
        if is_delete is False:
            try:
                await delete_message(chat_id=1, message_id=1)
            except Exception as e:
                assert isinstance(e, error)
        else:
            await delete_message(chat_id=1, message_id=1)

        assert mock_bot.delete_message.call_count == 1
