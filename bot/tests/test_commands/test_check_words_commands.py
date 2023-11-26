from unittest.mock import AsyncMock, MagicMock, patch

from aiogram.types import CallbackQuery, User, Message
from pytest import mark

from bot import bot
from choices import State
from commands import handle_check_words_other_data


class TestCheckWordsCommand:
    """Tests command check words."""

    @mark.asyncio
    async def test_handle_check_words_other_data_callback(self, monkeypatch):
        chat_id = 1
        monkeypatch.setattr('commands.registration.State', MagicMock(value=State.check_words.value))
        user = User(id=chat_id, is_bot=False, first_name="Test User")
        mock_callback = CallbackQuery(id=1, chat=chat_id, data='other_data', from_user=user)
        mock_callback.from_user = user

        with patch.object(bot, 'send_message', new=AsyncMock()) as mock_send_message:
            await handle_check_words_other_data(mock_callback)

            expected_text = 'Нужно нажать по кнопке I know или I don\'t know'

            mock_send_message.assert_called_once_with(chat_id=chat_id, text=expected_text)
