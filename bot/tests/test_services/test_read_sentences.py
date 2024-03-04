from copy import deepcopy

from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup, KeyboardButton, User, ParseMode
from pytest import mark, fixture
from unittest.mock import ANY, AsyncMock, mock_open, patch

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

    @mark.asyncio
    async def test_create_file_path(self):
        self._service._telegram_user = self._telegram_user
        await self._service._create_file_path()
        file_name = f'{self._telegram_user.new_sentence.book_id} - {self._telegram_user.new_sentence.order}'
        expected_file_path = f'static/audio/{file_name}.mp3'
        assert self._service._file_path == expected_file_path

    @mark.parametrize('number, is_exist_file', [[1, True], [2, True], [1, False], [3, False]])
    @patch('services.read_sentence.randint')
    @patch('services.read_sentence.path.isfile')
    @mark.asyncio
    async def test_create_message_text(self, mock_path, mock_randint, number, is_exist_file):
        mock_send_audio_message = AsyncMock(return_value=None)
        self._service._send_audio_message = mock_send_audio_message

        mock_randint.return_value = number
        mock_path.return_value = is_exist_file
        self._service._telegram_user = self._telegram_user
        self._service._file_path = 'test_file'
        sentence_text = 'Hello World!'
        translate_text = 'Привет мир!'
        self._service._sentence_text = sentence_text
        self._service._sentence_translation = translate_text
        await self._service._create_message_text()

        if is_exist_file and number == 1:
            self._service._send_audio_message.assert_called_once()
        else:
            self._service._send_audio_message.assert_not_called()
            expected_text = f'{sentence_text}\n\n<tg-spoiler>{translate_text}</tg-spoiler>'
            self._service._message_text = expected_text

    @mark.parametrize('number', [i for i in range(1, 7)])
    @patch('services.read_sentence.randint')
    @mark.asyncio
    async def test_send_message_or_tenses(self, mock_randint, number):
        mock_send_tenses = AsyncMock(return_value=None)
        self._service._send_tenses = mock_send_tenses

        mock_randint.return_value = number

        mock_send_message = AsyncMock(return_value=None)
        self._service._send_message = mock_send_message

        await self._service._send_message_or_tenses()

        if number == 1:
            self._service._send_tenses.assert_called_once()
            self._service._send_message.assert_not_called()
        else:
            self._service._send_tenses.assert_not_called()
            self._service._send_message.assert_called_once()

    @patch('builtins.open', new_callable=mock_open, read_data='data')
    @patch('services.read_sentence.bot', new_callable=AsyncMock)
    @mark.asyncio
    async def test_send_audio_message(self, mock_bot, mock_open_file):
        self._service._file_path = 'test_file'
        self._service._sentence_text = 'Hello World!'
        self._service._sentence_translation = 'Привет мир!'
        self._service._telegram_user = self._telegram_user
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton(text='test'))
        self._service._keyboard = keyboard

        await self._service._send_audio_message()

        mock_open_file.assert_called_once()
        expected_text = 'Text:\n\n<tg-spoiler>Hello World!</tg-spoiler>'
        expected_message = 'Translate:\n\n<tg-spoiler>Привет мир!</tg-spoiler>'
        assert self._service._message_text == expected_message
        mock_bot.send_audio.assert_called_once_with(
            chat_id=self._telegram_user.telegram_id,
            audio=ANY,
            caption=expected_text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard,
        )

    @mark.parametrize('is_update', [True, False])
    @mark.asyncio
    async def test_send_tenses(self, is_update):
        mock_update_stage_user = AsyncMock(return_value=is_update)
        self._service._update_stage_user = mock_update_stage_user

        mock_send_text_with_tenses = AsyncMock(return_values=None)
        self._service._send_text_with_tenses = mock_send_text_with_tenses

        await self._service._send_tenses()

        if is_update:
            mock_update_stage_user.assert_called_once()
            mock_send_text_with_tenses.assert_called_once()
        else:
            mock_update_stage_user.assert_called_once()
            mock_send_text_with_tenses.assert_not_called()

    @mark.parametrize('is_update', [True, False])
    @patch('services.read_sentence.bot', new_callable=AsyncMock)
    @patch('services.read_sentence.delete_message')
    @mark.asyncio
    async def test_send_message(self, mock_delete_message, mock_bot, is_update):
        mock_update_history_sentence = AsyncMock(return_value=is_update)
        self._service._update_history_sentence = mock_update_history_sentence

        self._service._telegram_user = self._telegram_user
        self._service._message_text = 'Test'
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='Test'))
        self._service._keyboard = keyboard

        await self._service._send_message()

        if is_update:
            mock_update_history_sentence.assert_called_once()
            mock_delete_message.assert_called_once()
            mock_bot.send_message.assert_called_once_with(
                chat_id=self._telegram_user.telegram_id,
                text='Test',
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard,
            )
        else:
            mock_update_history_sentence.assert_called_once()
            mock_delete_message.assert_not_called()
            mock_bot.send_message.assert_not_called()