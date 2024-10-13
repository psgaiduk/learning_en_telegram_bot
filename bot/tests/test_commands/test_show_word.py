from unittest.mock import AsyncMock, Mock, patch

from aiogram.types import (
    ParseMode,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from pytest import mark

from bot import bot
from choices import State
from commands import (
    handle_show_word,
    handle_show_word_other_data,
)
from tests.fixtures import *


class TestShowWordCommand:
    """Tests command show word."""

    @patch("commands.show_word.update_data_by_api", new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_update_profile(self, mock_update_user, telegram_user_with_sentence_and_word_and_learn_word):
        chat_id = 1
        telegram_user = telegram_user_with_sentence_and_word_and_learn_word
        word = telegram_user.learn_words[0]
        callback = AsyncMock()
        callback.data = "another_data"
        callback.from_user.id = chat_id
        callback.message.message_id = 1
        callback.message.chat.id = chat_id
        state = AsyncMock()
        state.get_data = AsyncMock(return_value={"telegram_user": telegram_user})
        mock_update_user.side_effect = [True]

        translate_word = word.translation.get("ru")
        expected_text = f"{'=' * 35}\n\n" f"{word.word}\n\n" f"<b><u>{translate_word}</u></b>\n\n" f"{'=' * 35}\n"

        with patch.object(bot, "edit_message_text", new=AsyncMock()) as mock_edit_message:

            await handle_show_word(callback_query=callback, state=state)
            expected_keyboard = InlineKeyboardMarkup()
            expected_keyboard.add(InlineKeyboardButton(text="Помню", callback_data="learn_word_yes"))
            expected_keyboard.add(InlineKeyboardButton(text="Не помню", callback_data="learn_word_no"))
            mock_edit_message.assert_called_once_with(
                chat_id=chat_id,
                message_id=1,
                text=expected_text,
                parse_mode=ParseMode.HTML,
                reply_markup=expected_keyboard,
            )

            expected_data_for_update_user = {
                "telegram_id": chat_id,
                "stage": State.learn_words.value,
            }

            mock_update_user.assert_awaited_once_with(
                telegram_id=chat_id,
                params_for_update=expected_data_for_update_user,
                url_for_update=f"telegram_user/{chat_id}",
            )

    @mark.asyncio
    async def test_handle_show_word_other_data_callback(self):
        chat_id = 1
        callback = Mock()
        callback.data = "another_data"
        callback.from_user.id = chat_id

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:

            await handle_show_word_other_data(message_data=callback)

            mock_send_message.assert_called_once_with(
                chat_id=chat_id,
                text='Нужно нажать по кнопке "Проверить"',
            )

    @mark.asyncio
    async def test_handle_show_word_other_data_message(self):
        chat_id = 1
        message = Mock()
        message.text = "/profile"
        message.from_user.id = chat_id

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:

            await handle_show_word_other_data(message_data=message)

            mock_send_message.assert_called_once_with(
                chat_id=chat_id,
                text='Нужно нажать по кнопке "Проверить"',
            )
