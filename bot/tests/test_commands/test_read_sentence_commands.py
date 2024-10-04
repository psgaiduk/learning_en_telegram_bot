from unittest.mock import AsyncMock, patch, call, ANY, mock_open

from aiogram.types import (
    CallbackQuery,
    Message,
    ParseMode,
    ReplyKeyboardMarkup,
    KeyboardButton,
    User,
    ReplyKeyboardRemove,
)
from pytest import mark

from bot import bot
from choices import State
from commands import (
    handle_read_sentence,
    handle_read_sentence_other_data,
    handle_end_read_sentence_today,
)
from tests.fixtures import *


class TestReadSentenceCommand:
    """Tests command read sentence."""

    @mark.asyncio
    async def test_handle_read_sentence_other_data_callback(self):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name="Test User")
        mock_callback = CallbackQuery(id=1, chat=chat_id, data="other_data", from_user=user)
        mock_callback.from_user = user

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:
            await handle_read_sentence_other_data(mock_callback)
            expected_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            expected_keyboard.add(KeyboardButton(text="Read"))
            expected_text = "Нужно нажать по кнопке Read"
            mock_send_message.assert_called_once_with(
                chat_id=chat_id,
                text=expected_text,
                reply_markup=expected_keyboard,
                parse_mode=ParseMode.HTML,
            )

    @mark.asyncio
    async def test_handle_read_sentence_other_data_message(self):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name="Test User")
        mock_message = Message(id=1, chat=chat_id, text="Read", from_user=user)
        mock_message.from_user = user

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:
            await handle_read_sentence_other_data(mock_message)
            expected_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            expected_keyboard.add(KeyboardButton(text="Read"))
            expected_text = "Нужно нажать по кнопке Read"
            mock_send_message.assert_called_once_with(
                chat_id=chat_id,
                text=expected_text,
                reply_markup=expected_keyboard,
                parse_mode=ParseMode.HTML,
            )

    @patch("commands.read_sentence.ReadSentenceService.do")
    @mark.asyncio
    async def test_handle_just_read_sentence(self, mock_read_sentence_service):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name="Test User")
        mock_callback = CallbackQuery(id=1, chat=chat_id, data="other_data", from_user=user, message=Message(id=1))
        mock_callback.from_user = user
        state = AsyncMock()

        await handle_read_sentence(message=mock_callback, state=state)

        mock_read_sentence_service.assert_called_once()

    @patch("commands.read_sentence.send_message_end_read_today_func")
    @mark.asyncio
    async def test_handle_end_read_sentence_today_message(self, mock_send_message_end_read_today_func):
        chat_id = 1
        state = AsyncMock()
        user = User(id=chat_id, is_bot=False, first_name="Test User")
        mock_message = Message(id=1, chat=chat_id, text="Read", from_user=user)
        mock_message.from_user = user

        await handle_end_read_sentence_today(mock_message, state=state)
        mock_send_message_end_read_today_func.assert_called_once_with(message=mock_message, state=state)

    @patch("commands.read_sentence.send_message_end_read_today_func")
    @mark.asyncio
    async def test_handle_end_read_sentence_today_callback(self, mock_send_message_end_read_today_func):
        chat_id = 1
        state = AsyncMock()
        user = User(id=chat_id, is_bot=False, first_name="Test User")
        mock_callback = CallbackQuery(id=1, chat=chat_id, data="other_data", from_user=user)
        mock_callback.from_user = user

        await handle_end_read_sentence_today(message=mock_callback, state=state)
        mock_send_message_end_read_today_func.assert_called_once_with(message=mock_callback, state=state)
