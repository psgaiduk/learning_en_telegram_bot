from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytest import mark
from unittest.mock import ANY, AsyncMock, patch

from bot import bot
from services import UpdateProfileService


class TestCheckWordsService:
    """Tests for CheckWordsService."""

    def setup_method(self):
        self._state = AsyncMock()
        self._chat_id = 12345

    @mark.parametrize("start_message_text", ["", "test"])
    @mark.asyncio
    async def test_do(self, start_message_text):
        service = UpdateProfileService(chat_id=self._chat_id, start_message_text=start_message_text)

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:
            await service.do()

            excepted_text = (
                f"{start_message_text}"
                f"Вы можете изменить своё имя или уровень английского языка.\n"
                f"Чтобы выйти из изменения профиля кликните по кнопке close."
            )

            mock_send_message.assert_called_once_with(
                chat_id=self._chat_id,
                text=excepted_text,
                reply_markup=ANY,
            )

            reply_markup_call = mock_send_message.call_args_list[0]
            reply_markup = reply_markup_call.kwargs["reply_markup"]

            assert isinstance(reply_markup, InlineKeyboardMarkup)
            assert reply_markup.inline_keyboard == [
                [
                    InlineKeyboardButton(
                        text="Change english level",
                        callback_data="user_profile_change_en_level",
                    )
                ],
                [InlineKeyboardButton(text="Change name", callback_data="user_profile_change_name")],
                [InlineKeyboardButton(text="Close", callback_data="user_profile_close")],
            ]
