from unittest.mock import AsyncMock, patch, call

from aiogram.types import (
    Message,
    ParseMode,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    User,
)
from pytest import mark

from bot import bot
from functions import send_message_end_read_today_func
from tests.fixtures import *


class TestEndReadTodayFunction:
    """Tests send message if end read today function."""

    @patch("functions.end_read_sentence_today.delete_message")
    @mark.asyncio
    async def test_send_message_if_end_sentences(self, mock_delete_message):
        chat_id = 1
        state = AsyncMock()
        user = User(id=chat_id, is_bot=False, first_name="Test User")
        mock_message = Message(id=1, chat=chat_id, text="Read", from_user=user)
        mock_message.from_user = user

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:
            await send_message_end_read_today_func(message=mock_message, state=state)
            expected_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            expected_keyboard.add(KeyboardButton(text="Read"))
            expected_text = "Вы прочитали все предложения на сегодня. Новые предложения будут доступны завтра."
            expected_keyboard_second = InlineKeyboardMarkup()
            expected_keyboard_second.add(
                InlineKeyboardButton(text="Повторение слов", callback_data="learn_words_again")
            )
            expected_text_second = "Но можно продолжить повторение слов"

            mock_send_message.assert_has_calls(
                [
                    call(
                        chat_id=chat_id,
                        text=expected_text,
                        reply_markup=expected_keyboard,
                        parse_mode=ParseMode.HTML,
                    ),
                    call(
                        chat_id=chat_id,
                        text=expected_text_second,
                        reply_markup=expected_keyboard_second,
                        parse_mode=ParseMode.HTML,
                    ),
                ],
                any_order=False,
            )

            assert mock_send_message.call_count == 2

            mock_delete_message.assert_called_once_with(message=mock_message, state=state)
