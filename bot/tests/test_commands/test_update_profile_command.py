from unittest.mock import ANY, AsyncMock, Mock, patch

from pytest import mark

from bot import bot
from choices import State
from commands import (
    handle_update_profile,
    handle_update_profile_close,
    handle_update_profile_name,
    handle_update_profile_en_level,
    handle_update_profile_other_data,
)
from dto import HeroLevelDTOModel, TelegramUserDTOModel


class TestUpdateProfileCommand:
    """Tests command update profile."""

    @patch("commands.update_profile.UpdateProfileService")
    @patch("commands.update_profile.update_data_by_api", new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_update_profile(self, mock_update_user, mock_update_profile_service):
        chat_id = 1
        message = Mock()
        message.text = "/profile"
        message.from_user.id = chat_id
        mock_update_user.side_effect = [True]

        mock_update_profile_service.return_value.do = AsyncMock()

        await handle_update_profile(message)

        mock_update_profile_service.assert_called_once_with(chat_id=chat_id, start_message_text="")
        mock_update_profile_service.return_value.do.assert_called_once()

        expected_data_for_update_user = {
            "telegram_id": chat_id,
            "stage": State.update_profile.value,
        }

        mock_update_user.assert_awaited_once_with(
            telegram_id=chat_id,
            params_for_update=expected_data_for_update_user,
            url_for_update=f"telegram_user/{chat_id}",
        )

    @patch("commands.update_profile.UpdateProfileService")
    @patch("commands.update_profile.update_data_by_api", new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_update_profile_with_mistake(self, mock_update_user, mock_update_profile_service):
        chat_id = 1
        message = Mock()
        message.text = "/profile"
        message.from_user.id = chat_id
        mock_update_user.side_effect = [False]

        mock_update_profile_service.return_value.do = AsyncMock()

        await handle_update_profile(message)

        mock_update_profile_service.assert_not_called()

        expected_data_for_update_user = {
            "telegram_id": chat_id,
            "stage": State.update_profile.value,
        }

        mock_update_user.assert_awaited_once_with(
            telegram_id=chat_id,
            params_for_update=expected_data_for_update_user,
            url_for_update=f"telegram_user/{chat_id}",
        )

    @patch("commands.update_profile.update_data_by_api", new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_update_profile_name(self, mock_update_user):
        chat_id = 1
        callback = Mock()
        callback.data = "user_profile_change_name"
        callback.from_user.id = chat_id
        mock_update_user.side_effect = [True]

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:
            await handle_update_profile_name(callback)

            mock_send_message.assert_called_once_with(chat_id=chat_id, text="Введите ваше имя:")

            expected_data_for_update_user = {
                "telegram_id": chat_id,
                "stage": State.wait_name.value,
            }

            mock_update_user.assert_awaited_once_with(
                telegram_id=chat_id,
                params_for_update=expected_data_for_update_user,
                url_for_update=f"telegram_user/{chat_id}",
            )

    @patch("commands.update_profile.update_data_by_api", new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_update_profile_name_with_mistake(self, mock_update_user):
        chat_id = 1
        callback = Mock()
        callback.data = "user_profile_change_name"
        callback.from_user.id = chat_id
        mock_update_user.side_effect = [False]

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:
            await handle_update_profile_name(callback)

            mock_send_message.assert_not_awaited()

            expected_data_for_update_user = {
                "telegram_id": chat_id,
                "stage": State.wait_name.value,
            }

            mock_update_user.assert_awaited_once_with(
                telegram_id=chat_id,
                params_for_update=expected_data_for_update_user,
                url_for_update=f"telegram_user/{chat_id}",
            )

    @patch("commands.update_profile.create_keyboard_for_en_levels", new_callable=AsyncMock)
    @patch("commands.update_profile.update_data_by_api", new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_update_profile_change_level(self, mock_update_user, mock_create_keyboard_for_en_levels):
        chat_id = 1
        callback = Mock()
        callback.data = "user_profile_change_en_level"
        callback.from_user.id = chat_id
        hero_level_order = 1
        mock_update_user.side_effect = [True]

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:

            hero_level = HeroLevelDTOModel(
                id=1,
                title="Level",
                order=hero_level_order,
                need_experience=0,
                count_sentences=0,
                count_games=0,
            )

            telegram_user_model = TelegramUserDTOModel(
                telegram_id=chat_id,
                user_name="UserName",
                experience=10,
                previous_stage="PreviousStage",
                stage="CurrentStage",
                main_language=None,
                level_en=None,
                hero_level=hero_level,
            )

            state = Mock()
            state.get_data = AsyncMock(return_value={"telegram_user": telegram_user_model})

            await handle_update_profile_en_level(callback_query=callback, state=state)

            mock_create_keyboard_for_en_levels.assert_called_once_with(hero_level=hero_level_order)

            mock_send_message.assert_called_once_with(
                chat_id=chat_id,
                text="Выберите уровень сложности: ",
                reply_markup=ANY,
            )

            expected_data_for_update_user = {
                "telegram_id": chat_id,
                "stage": State.wait_en_level.value,
            }

            mock_update_user.assert_awaited_once_with(
                telegram_id=chat_id,
                params_for_update=expected_data_for_update_user,
                url_for_update=f"telegram_user/{chat_id}",
            )

    @patch("commands.update_profile.create_keyboard_for_en_levels", new_callable=AsyncMock)
    @patch("commands.update_profile.update_data_by_api", new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_update_profile_change_level_with_mistake(
        self, mock_update_user, mock_create_keyboard_for_en_levels
    ):
        chat_id = 1
        callback = Mock()
        callback.data = "user_profile_change_en_level"
        callback.from_user.id = chat_id
        hero_level_order = 1
        mock_update_user.side_effect = [False]

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:

            hero_level = HeroLevelDTOModel(
                id=1,
                title="Level",
                order=hero_level_order,
                need_experience=0,
                count_sentences=0,
                count_games=0,
            )

            telegram_user_model = TelegramUserDTOModel(
                telegram_id=chat_id,
                user_name="UserName",
                experience=10,
                previous_stage="PreviousStage",
                stage="CurrentStage",
                main_language=None,
                level_en=None,
                hero_level=hero_level,
            )

            state = Mock()
            state.get_data = AsyncMock(return_value={"telegram_user": telegram_user_model})

            await handle_update_profile_en_level(callback_query=callback, state=state)

            mock_create_keyboard_for_en_levels.assert_not_called()

            mock_send_message.assert_not_awaited()

            expected_data_for_update_user = {
                "telegram_id": chat_id,
                "stage": State.wait_en_level.value,
            }

            mock_update_user.assert_awaited_once_with(
                telegram_id=chat_id,
                params_for_update=expected_data_for_update_user,
                url_for_update=f"telegram_user/{chat_id}",
            )

    @patch("commands.update_profile.update_data_by_api", new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_update_profile_close(self, mock_update_user):
        chat_id = 1
        callback = Mock()
        callback.data = "user_profile_close"
        callback.from_user.id = chat_id
        mock_update_user.side_effect = [True]
        expected_previous_stage = "PreviousStage"

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:
            hero_level = HeroLevelDTOModel(
                id=1,
                title="Level",
                order=1,
                need_experience=0,
                count_sentences=0,
                count_games=0,
            )

            telegram_user_model = TelegramUserDTOModel(
                telegram_id=chat_id,
                user_name="UserName",
                experience=10,
                previous_stage=expected_previous_stage,
                stage="CurrentStage",
                main_language=None,
                level_en=None,
                hero_level=hero_level,
            )

            state = Mock()
            state.get_data = AsyncMock(return_value={"telegram_user": telegram_user_model})

            await handle_update_profile_close(callback_query=callback, state=state)

            mock_send_message.assert_called_once_with(
                chat_id=chat_id,
                text="Настройка профиля завершена.",
            )

            expected_data_for_update_user = {
                "telegram_id": chat_id,
                "previous_stage": "",
                "stage": expected_previous_stage,
            }

            mock_update_user.assert_awaited_once_with(
                telegram_id=chat_id,
                params_for_update=expected_data_for_update_user,
                url_for_update=f"telegram_user/{chat_id}",
            )

    @patch("commands.update_profile.update_data_by_api", new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_update_profile_close_with_mistake(self, mock_update_user):
        chat_id = 1
        callback = Mock()
        callback.data = "user_profile_close"
        callback.from_user.id = chat_id
        mock_update_user.side_effect = [False]
        expected_previous_stage = "PreviousStage"

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:
            hero_level = HeroLevelDTOModel(
                id=1,
                title="Level",
                order=1,
                need_experience=0,
                count_sentences=0,
                count_games=0,
            )

            telegram_user_model = TelegramUserDTOModel(
                telegram_id=chat_id,
                user_name="UserName",
                experience=10,
                previous_stage=expected_previous_stage,
                stage="CurrentStage",
                main_language=None,
                level_en=None,
                hero_level=hero_level,
            )

            state = Mock()
            state.get_data = AsyncMock(return_value={"telegram_user": telegram_user_model})

            await handle_update_profile_close(callback_query=callback, state=state)

            mock_send_message.assert_not_awaited()

            expected_data_for_update_user = {
                "telegram_id": chat_id,
                "previous_stage": "",
                "stage": expected_previous_stage,
            }

            mock_update_user.assert_awaited_once_with(
                telegram_id=chat_id,
                params_for_update=expected_data_for_update_user,
                url_for_update=f"telegram_user/{chat_id}",
            )

    @mark.asyncio
    async def test_handle_update_profile_other_data(self):
        chat_id = 1
        callback = Mock()
        callback.data = "user_profile_"
        callback.from_user.id = chat_id

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:

            await handle_update_profile_other_data(callback_query=callback)

            mock_send_message.assert_called_once_with(
                chat_id=chat_id,
                text="Нужно кликнуть по кнопке, чтобы продолжить настройку профиля.",
            )
