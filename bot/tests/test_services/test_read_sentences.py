from copy import deepcopy

from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup, KeyboardButton, User
from pytest import mark, fixture
from unittest.mock import ANY, AsyncMock, patch

from bot import bot
from choices import EnglishLevels, State
from services import ReadSentenceService
from tests.fixtures import *


class TestReadSentenceService:
    """Tests for ReadSentenceService."""

    @fixture(autouse=True)
    def setup_method(self, telegram_user_with_sentence_and_word):
        self._state = AsyncMock()
        self._telegram_user = telegram_user_with_sentence_and_word
        self._chat_id = self._telegram_user.telegram_id
        user = User(id=self._chat_id, is_bot=False, first_name='Test User')
        message = Message(id=1, chat=self._chat_id, text='Read', from_user=user)
        self._service = ReadSentenceService(message=message, state=self._state)

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

    @mark.asyncio
    @patch('services.read_sentence.save_word_history')
    async def test_do_message(self, mock_save_word_history):
        mock_get_telegram_user = AsyncMock(return_value=None)
        self._service._get_telegram_user = mock_get_telegram_user
        self._service._telegram_user = deepcopy(self._telegram_user)

        mock_get_sentence = AsyncMock(return_value=None)
        self._service._get_sentence = mock_get_sentence

        mock_create_keyboard = AsyncMock(return_value=None)
        self._service._create_keyboard = mock_create_keyboard

        mock_create_path_file = AsyncMock(return_value=None)
        self._service._create_file_path = mock_create_path_file

        mock_create_message_text = AsyncMock(return_value=None)
        self._service._create_message_text = mock_create_message_text

        mock_send_message_or_tenses = AsyncMock(return_value=None)
        self._service._send_message_or_tenses = mock_send_message_or_tenses

        assert self._service._telegram_user.new_sentence.text != ''
        await self._service.do()

        mock_get_telegram_user.assert_called_once()
        mock_get_sentence.assert_called_once()
        mock_create_keyboard.assert_called_once()
        mock_create_path_file.assert_called_once()
        mock_create_message_text.assert_called_once()
        mock_send_message_or_tenses.assert_called_once()

        mock_save_word_history.assert_not_called()
        assert self._service._telegram_user.new_sentence.text == ''

    @mark.asyncio
    async def test_get_user(self):

        self._state.get_data = AsyncMock(return_value={'user': self._telegram_user})

        await self._service._get_telegram_user()

        assert self._service._telegram_user == self._telegram_user

    @mark.parametrize('english_level', [level.level_order for level in EnglishLevels])
    @mark.asyncio
    async def test_get_sentence(self, english_level):

        self._telegram_user.level_en.order = english_level
        self._service._telegram_user = self._telegram_user

        await self._service._get_sentence()

        if english_level < EnglishLevels.B1.level_order:
            assert self._service._sentence_text == self._service._telegram_user.new_sentence.text_with_words
        else:
            assert self._service._sentence_text == self._service._telegram_user.new_sentence.text

        assert self._service._sentence_translation == self._telegram_user.new_sentence.translation.get('ru')

    @mark.asyncio
    async def test_create_keyboard(self):
        await self._service._create_keyboard()
        expected_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        expected_keyboard.add(KeyboardButton(text='Read'))
        assert self._service._keyboard == expected_keyboard
