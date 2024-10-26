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
    handle_end_read_sentence_today_after_learn_words,
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

    @patch("commands.read_sentence.EndReadTodayService.work")
    @mark.asyncio
    async def test_handle_end_read_sentence_today_message(self, mock_send_message_end_read_today_service):
        chat_id = 1
        state = AsyncMock()
        user = User(id=chat_id, is_bot=False, first_name="Test User")
        mock_message = Message(id=1, chat=chat_id, text="Read", from_user=user)
        mock_message.from_user = user

        await handle_end_read_sentence_today(mock_message, state=state)
        mock_send_message_end_read_today_service.assert_called_once()

    @patch("commands.read_sentence.EndReadTodayService.work")
    @mark.asyncio
    async def test_handle_end_read_sentence_today_callback(self, mock_send_message_end_read_today_service):
        chat_id = 1
        state = AsyncMock()
        user = User(id=chat_id, is_bot=False, first_name="Test User")
        mock_callback = CallbackQuery(id=1, chat=chat_id, data="other_data", from_user=user)
        mock_callback.from_user = user

        await handle_end_read_sentence_today(message=mock_callback, state=state)
        mock_send_message_end_read_today_service.assert_called_once()

    @patch("commands.read_sentence.EndReadTodayService.work")
    @patch("commands.read_sentence.update_learn_word")
    @mark.asyncio
    async def test_handle_end_read_sentence_today_after_learn_words(
        self,
        mock_update_learn_word,
        mock_send_message_end_read_today_service,
        telegram_user_with_sentence_and_word_and_learn_word,
    ):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name="Test User")
        mock_callback = CallbackQuery(id=1, chat=chat_id, data="other_data", from_user=user, message=Message(id=1))
        mock_callback.from_user = user
        state = AsyncMock()
        telegram_user = telegram_user_with_sentence_and_word_and_learn_word
        state.get_data = AsyncMock(return_value={"telegram_user": telegram_user})
        expected_learn_word = telegram_user.learn_words[0]
        expected_telegram_user = telegram_user_with_sentence_and_word_and_learn_word

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:
            await handle_end_read_sentence_today_after_learn_words(message=mock_callback, state=state)
            mock_send_message_end_read_today_service.assert_called_once()
            mock_update_learn_word.assert_called_once_with(
                message=mock_callback,
                word=expected_learn_word,
            )
            mock_send_message.assert_not_called()
            expected_telegram_user.learn_words = []
            state.update_data.assert_called_once_with(telegram_user=expected_telegram_user)

    @patch("commands.read_sentence.EndReadTodayService.work", new_callable=AsyncMock)
    @patch("commands.read_sentence.update_learn_word")
    @mark.asyncio
    async def test_handle_end_read_sentence_today_after_learn_words_without_words(
        self,
        mock_update_learn_word,
        mock_send_message_end_read_today_service,
        telegram_user_with_sentence_and_word_and_learn_word,
    ):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name="Test User")
        mock_callback = CallbackQuery(id=1, chat=chat_id, data="other_data", from_user=user, message=Message(id=1))
        mock_callback.from_user = user
        state = AsyncMock()
        telegram_user = telegram_user_with_sentence_and_word_and_learn_word
        telegram_user.learn_words = []
        state.get_data = AsyncMock(return_value={"telegram_user": telegram_user})

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:
            await handle_end_read_sentence_today_after_learn_words(message=mock_callback, state=state)
            mock_send_message_end_read_today_service.assert_called_once()
            mock_update_learn_word.assert_not_called()
            mock_send_message.assert_not_called()
            state.update_data.assert_not_called()

    @patch("commands.read_sentence.EndReadTodayService.work", new_callable=AsyncMock)
    @patch("commands.read_sentence.update_learn_word")
    @mark.asyncio
    async def test_handle_end_read_sentence_today_after_learn_words_with_error_update(
        self,
        mock_update_learn_word,
        mock_send_message_end_read_today_service,
        telegram_user_with_sentence_and_word_and_learn_word,
    ):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name="Test User")
        mock_callback = CallbackQuery(id=1, chat=chat_id, data="other_data", from_user=user, message=Message(id=1))
        mock_callback.from_user = user
        state = AsyncMock()
        telegram_user = telegram_user_with_sentence_and_word_and_learn_word
        state.get_data = AsyncMock(return_value={"telegram_user": telegram_user})
        expected_learn_word = telegram_user.learn_words[0]
        mock_update_learn_word.return_value = False

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:
            await handle_end_read_sentence_today_after_learn_words(message=mock_callback, state=state)
            mock_send_message_end_read_today_service.assert_not_called()
            mock_update_learn_word.assert_called_once_with(
                message=mock_callback,
                word=expected_learn_word,
            )
            mock_send_message.assert_called_once_with(
                chat_id=chat_id,
                text="Что-то пошло не так, попробуй ещё раз",
            )
            state.update_data.assert_not_called()
