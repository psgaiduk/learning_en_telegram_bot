from unittest.mock import AsyncMock, MagicMock, patch

from aiogram.types import CallbackQuery, Message, ParseMode, ReplyKeyboardMarkup, KeyboardButton, User
from pytest import mark

from bot import bot
from commands import handle_read_sentence_other_data


class TestReadSentenceCommand:
    """Tests command read sentence."""

    @mark.asyncio
    async def test_handle_read_sentence_other_data_callback(self):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name='Test User')
        mock_callback = CallbackQuery(id=1, chat=chat_id, data='other_data', from_user=user)
        mock_callback.from_user = user

        with patch.object(bot, 'send_message', new=AsyncMock()) as mock_send_message:
            await handle_read_sentence_other_data(mock_callback)
            expected_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            expected_keyboard.add(KeyboardButton(text='Read'))
            expected_text = 'Нужно нажать по кнопке Read'
            mock_send_message.assert_called_once_with(chat_id=chat_id, text=expected_text, reply_markup=expected_keyboard, parse_mode=ParseMode.HTML)

    @mark.asyncio
    async def test_handle_read_sentence_other_data_message(self):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name='Test User')
        mock_message = Message(id=1, chat=chat_id, text='Read', from_user=user)
        mock_message.from_user = user

        with patch.object(bot, 'send_message', new=AsyncMock()) as mock_send_message:
            await handle_read_sentence_other_data(mock_message)
            expected_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            expected_keyboard.add(KeyboardButton(text='Read'))
            expected_text = 'Нужно нажать по кнопке Read'
            mock_send_message.assert_called_once_with(chat_id=chat_id, text=expected_text, reply_markup=expected_keyboard, parse_mode=ParseMode.HTML)

