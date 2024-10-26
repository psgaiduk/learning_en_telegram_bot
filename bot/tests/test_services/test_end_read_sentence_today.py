from unittest.mock import AsyncMock, patch, call

from aiogram.types import (
    Chat,
    Message,
    ParseMode,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    User,
)
from pytest import fixture, mark

from bot import bot
from services import EndReadTodayService
from tests.fixtures import *


class TestEndReadTodayService:
    """Tests send message if end read today service."""

    @fixture(autouse=True)
    def setup_method(self):
        self.state = AsyncMock()
        self.chat_id = 1
        user = User(id=self.chat_id, is_bot=False, first_name="Test User")
        self.mock_message = Message(id=1, text="Read", from_user=user)
        self.mock_message.from_user = user
        self.mock_message.chat = Chat(id=self.chat_id)
        self.mock_message.chat.id = self.chat_id
        self.service = EndReadTodayService(message=self.mock_message, state=self.state)

    @mark.parametrize("minutes_for_word", [0, 1])
    @patch("services.end_read_today.delete_message")
    @mark.asyncio
    async def test_send_message_if_end_sentences(self, mock_delete_message, minutes_for_word):

        self.service.messages_for_delete = []
        mock_get_messages_for_delete = AsyncMock(return_value=None)
        self.service._get_messages_for_delete = mock_get_messages_for_delete
        mock_send_message_end_sentences = AsyncMock(return_value=None)
        self.service._send_message_end_sentences = mock_send_message_end_sentences
        mock_get_user_stats = AsyncMock(return_value=None)
        self.service._get_user_stats = mock_get_user_stats
        self.service.minutes_for_repeat_word = minutes_for_word
        mock_send_message_repeat_words = AsyncMock(return_value=None)
        self.service._send_message_repeat_words = mock_send_message_repeat_words

        await self.service.work()

        mock_delete_message.assert_called_once_with(message=self.mock_message, state=self.state)
        self.state.update_data.assert_called_once_with(messages_for_delete=[])
        mock_get_messages_for_delete.assert_called_once()
        mock_send_message_end_sentences.assert_called_once()
        if minutes_for_word == 0:
            mock_send_message_repeat_words.assert_called_once()
        else:
            mock_send_message_repeat_words.assert_not_called()

    @mark.parametrize("state_data, expected_ids", [[{}, []], [{"messages_for_delete": [3]}, [3]]])
    @mark.asyncio
    async def test_get_messages_for_delete(self, state_data, expected_ids) -> None:
        self.state.get_data = AsyncMock(return_value=state_data)
        await self.service._get_messages_for_delete()
        assert self.service.messages_for_delete == expected_ids

    @mark.parametrize("old_messages_ids, expected_ids", [[[], [1]], [[3], [3, 1]]])
    @mark.asyncio
    async def test_send_message_end_sentence(self, old_messages_ids, expected_ids) -> None:
        self.service.messages_for_delete = old_messages_ids
        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:

            mock_send_message.side_effect = [AsyncMock(message_id=1)]
            await self.service._send_message_end_sentences()
            expected_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            expected_keyboard.add(KeyboardButton(text="Read"))
            expected_text = "Вы прочитали все предложения на сегодня. Новые предложения будут доступны завтра."

            mock_send_message.assert_called_once_with(
                chat_id=self.chat_id,
                text=expected_text,
                parse_mode=ParseMode.HTML,
                reply_markup=expected_keyboard,
            )

            assert self.service.messages_for_delete == expected_ids

    @mark.parametrize("old_messages_ids, expected_ids", [[[], [2]], [[3], [3, 2]]])
    @mark.asyncio
    async def test_send_message_repeat_words(self, old_messages_ids, expected_ids) -> None:
        self.service.messages_for_delete = old_messages_ids
        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:

            mock_send_message.side_effect = [AsyncMock(message_id=2)]

            expected_keyboard_second = InlineKeyboardMarkup()
            expected_keyboard_second.add(
                InlineKeyboardButton(text="Повторение слов", callback_data="learn_words_again")
            )
            expected_text_second = "Но можно продолжить повторение слов"

            await self.service._send_message_repeat_words()

            mock_send_message.assert_called_once_with(
                chat_id=self.chat_id,
                text=expected_text_second,
                parse_mode=ParseMode.HTML,
                reply_markup=expected_keyboard_second,
            )

            assert self.service.messages_for_delete == expected_ids

    @mark.parametrize("count_minutes_to_repeat", [0, 2])
    @patch("services.end_read_today.get_data_by_api_func")
    @mark.asyncio
    async def test_get_user_stats(self, mock_get_data_by_api_func, count_minutes_to_repeat, api_get_user_stats) -> None:
        api_get_user_stats["time_to_next_word"] = count_minutes_to_repeat
        mock_get_data_by_api_func.return_value = api_get_user_stats
        await self.service._get_user_stats()
        assert self.service.minutes_for_repeat_word == count_minutes_to_repeat
