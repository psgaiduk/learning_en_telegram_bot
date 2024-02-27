from copy import deepcopy

from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, User
from pytest import mark, fixture
from unittest.mock import ANY, AsyncMock, patch

from bot import bot
from choices import State
from services import ReadSentenceService
from tests.fixtures import *


class TestReadSentenceService:
    """Tests for ReadSentenceService."""

    @fixture(autouse=True)
    def setup_method(self, telegram_user_with_sentence_and_word):
        self._state = AsyncMock()
        self._telegram_user = telegram_user_with_sentence_and_word
        self._chat_id = self._telegram_user.telegram_id

    @mark.asyncio
    @patch('services.read_sentence.save_word_history')
    async def test_do_callback(self, mock_save_word_history):
        user = User(id=self._chat_id, is_bot=False, first_name='Test User')
        mock_callback = CallbackQuery(id=1, chat=self._chat_id, data='test_data', from_user=user)
        mock_callback.from_user = user
        service = ReadSentenceService(message=mock_callback, state=self._state)

        mock_get_telegram_user = AsyncMock(return_value=None)
        service._get_telegram_user = mock_get_telegram_user
        service._telegram_user = deepcopy(self._telegram_user)

        mock_get_sentence = AsyncMock(return_value=None)
        service._get_sentence = mock_get_sentence

        mock_create_keyboard = AsyncMock(return_value=None)
        service._create_keyboard = mock_create_keyboard

        mock_create_path_file = AsyncMock(return_value=None)
        service._create_file_path = mock_create_path_file

        mock_create_message_text = AsyncMock(return_value=None)
        service._create_message_text = mock_create_message_text

        mock_send_message_or_tenses = AsyncMock(return_value=None)
        service._send_message_or_tenses = mock_send_message_or_tenses

        assert service._telegram_user.new_sentence.text != ''
        await service.do()

        mock_get_telegram_user.assert_called_once()
        mock_get_sentence.assert_called_once()
        mock_create_keyboard.assert_called_once()
        mock_create_path_file.assert_called_once()
        mock_create_message_text.assert_called_once()
        mock_send_message_or_tenses.assert_called_once()

        mock_save_word_history.assert_called_once_with(callback_query=mock_callback)
        assert service._telegram_user.new_sentence.text == ''
