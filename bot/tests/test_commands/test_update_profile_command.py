from unittest.mock import AsyncMock, Mock, patch

from pytest import mark

from choices import State
from commands import handle_update_profile


class TestUpdateProfileCommand:
    """Tests command update profile."""

    @patch('commands.update_profile.UpdateProfileService')
    @patch('commands.update_profile.update_user', new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_update_profile(self, mock_update_user, mock_update_profile_service):
        chat_id = 1
        message = Mock()
        message.text = '/profile'
        message.from_user.id = chat_id
        mock_update_user.side_effect = [True]

        mock_update_profile_service.return_value.do = AsyncMock()

        await handle_update_profile(message)

        mock_update_profile_service.assert_called_once_with(chat_id=chat_id, start_message_text='')
        mock_update_profile_service.return_value.do.assert_called_once()

        expected_data_for_update_user = {
            'telegram_id': chat_id,
            'stage': State.update_profile.value,
        }

        mock_update_user.assert_awaited_once_with(
            telegram_id=chat_id,
            params_for_update=expected_data_for_update_user,
        )

    @patch('commands.update_profile.UpdateProfileService')
    @patch('commands.update_profile.update_user', new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_update_profile_with_mistake(self, mock_update_user, mock_update_profile_service):
        chat_id = 1
        message = Mock()
        message.text = '/profile'
        message.from_user.id = chat_id
        mock_update_user.side_effect = [False]

        mock_update_profile_service.return_value.do = AsyncMock()

        await handle_update_profile(message)

        mock_update_profile_service.assert_not_called()

        expected_data_for_update_user = {
            'telegram_id': chat_id,
            'stage': State.update_profile.value,
        }

        mock_update_user.assert_awaited_once_with(
            telegram_id=chat_id,
            params_for_update=expected_data_for_update_user,
        )
