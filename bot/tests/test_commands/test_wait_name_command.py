from unittest.mock import AsyncMock, Mock, patch

from pytest import mark

from bot import bot
from commands import (
    handle_wait_name,
    handle_wait_name_incorrect_work,
    handle_wait_name_incorrect_work_buttons,
)


class TestWaitNameCommand:
    """Tests command wait name."""

    @patch("commands.wait_name.WaitNameService")
    @mark.asyncio
    async def test_handle_wait_name(self, mock_wait_name_service):
        chat_id = 1
        message = Mock()
        message.text = "user_profile"
        message.from_user.id = chat_id
        state = Mock()

        mock_wait_name_service.return_value.do = AsyncMock()

        await handle_wait_name(message=message, state=state)

        mock_wait_name_service.assert_called_once_with(message=message, state=state)
        mock_wait_name_service.return_value.do.assert_called_once()

    @mark.asyncio
    async def test_handle_wait_name_button(self):
        chat_id = 1
        callback = Mock()
        callback.data = "test"
        callback.from_user.id = chat_id

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:

            await handle_wait_name_incorrect_work_buttons(callback_query=callback)

            mock_send_message.assert_called_once_with(
                chat_id=chat_id,
                text="Имя надо отправить как сообщение. Попробуйте еще раз.",
            )

    @mark.asyncio
    async def test_handle_wait_name_incorrect(self):
        chat_id = 1
        message = Mock()
        message.text = "test"
        message.from_user.id = chat_id

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:

            await handle_wait_name_incorrect_work(message=message)

            mock_send_message.assert_called_once_with(
                chat_id=chat_id,
                text="Имя надо вводить одним слово, без использования специальных символов. Попробуйте еще раз.",
            )
