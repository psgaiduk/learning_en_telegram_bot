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
        message = AsyncMock(message_id=1)
        message.from_user = AsyncMock(id=1)
        mock_bot.delete_message.side_effect = error
        if is_delete is False:
            try:
                await delete_message(message=message)
            except Exception as e:
                assert isinstance(e, error)
        else:
            await delete_message(message=message)

        assert mock_bot.delete_message.call_count == 1

    @patch('functions.send_and_delete_message.bot', new_callable=AsyncMock)
    @patch('functions.send_and_delete_message.delete_message')
    @mark.asyncio
    async def test_send_message_and_delete(self, mock_delete_message, mock_bot):
        chat_id = 1
        message_text = 'test'
        reply_markup = None

        message = AsyncMock(message_id=1)
        message.from_user = AsyncMock(id=1)
        mock_bot.send_message.return_value = message
        await send_message_and_delete(chat_id=chat_id, message_text=message_text, reply_markup=reply_markup)
        mock_bot.send_message.assert_called_once_with(chat_id=chat_id, text=message_text, reply_markup=reply_markup)
        mock_delete_message.assert_called_once_with(message=message)
