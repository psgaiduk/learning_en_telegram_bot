from pytest import mark
from unittest.mock import ANY, AsyncMock, Mock, patch

from choices import State
from dto import HeroLevelDTOModel, TelegramUserDTOModel
from services import WaitNameService


class TestWaitNameService:
    """Tests for WaitNameService."""

    @classmethod
    def setup_class(cls):
        cls._message = Mock()
        cls._post_method_target = 'context_managers.aio_http_client.AsyncHttpClient.post'
        cls._state = Mock()

    @mark.asyncio
    async def test_get_user(self, mocker):
        self._message.answer = AsyncMock()

        telegram_user_model = TelegramUserDTOModel(
            telegram_id=12345,
            user_name='UserName',
            experience=10,
            previous_stage='PreviousStage',
            stage='CurrentStage',
            main_language=None,
            level_en=None,
            hero_level=None,
        )
        self._state.get_data = AsyncMock(return_value={'telegram_user': telegram_user_model})

        self._service = WaitNameService(message=self._message, state=self._state)

        await self._service._get_user()
        assert self._service._telegram_user == telegram_user_model
        self._state.get_data.assert_awaited_once()

    @mark.parametrize('hero_level_order', [1, 2, 3, 4, 5, 6])
    @patch('services.wait_name.create_keyboard_for_en_levels', new_callable=AsyncMock)
    @patch('services.wait_name.update_data_by_api', new_callable=AsyncMock)
    @mark.asyncio
    async def test_update_name_for_new_client(self, mock_update_user, mock_create_keyboard_for_en_levels, hero_level_order):
        mock_update_user.side_effect = [True]
        chat_id = 12345
        self._message.text = 'NewName'
        self._message.answer = AsyncMock()
        self._message.from_user.id = chat_id

        hero_level = HeroLevelDTOModel(
            id=1,
            title='Level',
            order=hero_level_order,
            need_experience=0,
            count_sentences=0,
            count_games=0,
        )

        telegram_user_model = TelegramUserDTOModel(
            telegram_id=chat_id,
            user_name='UserName',
            experience=10,
            previous_stage='PreviousStage',
            stage='CurrentStage',
            main_language=None,
            level_en=None,
            hero_level=hero_level,
        )

        self._state.get_data = AsyncMock(return_value={'telegram_user': telegram_user_model})

        self._service = WaitNameService(message=self._message, state=self._state)
        self._service._telegram_user = telegram_user_model
        self._service._update_user = AsyncMock(return_value=True)

        await self._service._update_name_for_new_client()

        message_text = (
            'Имя профиля изменено на Newname.\n'
            'Выберите уровень знаний английского языка. Сейчас вам доступен только первый уровень, '
            'но потом откроются новые уровни знаний.'
        )

        mock_create_keyboard_for_en_levels.assert_called_once_with(hero_level=hero_level_order)

        self._message.answer.assert_called_with(
            text=message_text,
            reply_markup=ANY,
        )

        expected_data_for_update_user = {
            'telegram_id': chat_id,
            'user_name': 'Newname',
            'stage': State.wait_en_level.value,
        }

        mock_update_user.assert_awaited_once_with(
            telegram_id=chat_id,
            params_for_update=expected_data_for_update_user,
            url_for_update=f'telegram_user/{chat_id}',
        )

    @mark.parametrize('hero_level_order', [1, 2, 3, 4, 5, 6])
    @patch('services.wait_name.create_keyboard_for_en_levels', new_callable=AsyncMock)
    @patch('services.wait_name.update_data_by_api', new_callable=AsyncMock)
    @mark.asyncio
    async def test_update_name_for_new_client_mistake(self, mock_update_user, mock_create_keyboard_for_en_levels, hero_level_order):
        mock_update_user.side_effect = [False]

        self._message.text = 'NewName'
        self._message.answer = AsyncMock()
        chat_id = 12345
        self._message.from_user.id = chat_id

        hero_level = HeroLevelDTOModel(
            id=1,
            title='Level',
            order=hero_level_order,
            need_experience=0,
            count_sentences=0,
            count_games=0,
        )

        telegram_user_model = TelegramUserDTOModel(
            telegram_id=chat_id,
            user_name='UserName',
            experience=10,
            previous_stage='PreviousStage',
            stage='CurrentStage',
            main_language=None,
            level_en=None,
            hero_level=hero_level,
        )

        self._state.get_data = AsyncMock(return_value={'telegram_user': telegram_user_model})

        self._service = WaitNameService(message=self._message, state=self._state)
        self._service._telegram_user = telegram_user_model

        await self._service._update_name_for_new_client()

        expected_data_for_update_user = {
            'telegram_id': chat_id,
            'user_name': 'Newname',
            'stage': State.wait_en_level.value,
        }

        mock_update_user.assert_awaited_once_with(
            telegram_id=chat_id,
            params_for_update=expected_data_for_update_user,
            url_for_update=f'telegram_user/{chat_id}',
        )

        self._message.answer.assert_not_awaited()
        mock_create_keyboard_for_en_levels.assert_not_awaited()

    @patch('services.wait_name.UpdateProfileService')
    @patch('services.wait_name.update_data_by_api', new_callable=AsyncMock)
    @mark.asyncio
    async def test_update_name_for_old_client(self, mock_update_user, mock_update_profile):
        mock_update_user.side_effect = [True]

        chat_id = 12345
        self._message.text = 'NewName'
        self._message.answer = AsyncMock()
        self._message.from_user.id = chat_id

        hero_level = HeroLevelDTOModel(
            id=1,
            title='Level',
            order=1,
            need_experience=0,
            count_sentences=0,
            count_games=0,
        )

        telegram_user_model = TelegramUserDTOModel(
            telegram_id=chat_id,
            user_name='UserName',
            experience=10,
            previous_stage='PreviousStage',
            stage='CurrentStage',
            main_language=None,
            level_en=None,
            hero_level=hero_level,
        )

        self._state.get_data = AsyncMock(return_value={'telegram_user': telegram_user_model})

        self._service = WaitNameService(message=self._message, state=self._state)
        self._service._telegram_user = telegram_user_model
        mock_update_profile.return_value.do = AsyncMock()
        await self._service._update_name_for_old_client()

        expected_data_for_update_user = {
            'telegram_id': chat_id,
            'user_name': 'Newname',
            'stage': State.update_profile.value,
        }

        mock_update_user.assert_awaited_once_with(
            telegram_id=chat_id,
            params_for_update=expected_data_for_update_user,
            url_for_update=f'telegram_user/{chat_id}',
        )

        expected_start_message_text = '🤖 Имя обновлено.\n'
        mock_update_profile.assert_called_once_with(chat_id=chat_id, start_message_text=expected_start_message_text)
        mock_update_profile.return_value.do.assert_awaited_once()

    @patch('services.wait_name.UpdateProfileService.do', new_callable=AsyncMock)
    @patch('services.wait_name.update_data_by_api', new_callable=AsyncMock)
    @mark.asyncio
    async def test_update_name_for_old_client_with_mistake(self, mock_update_user, mock_update_profile):
        mock_update_user.side_effect = [False]

        chat_id = 12345
        self._message.text = 'NewName'
        self._message.answer = AsyncMock()
        self._message.from_user.id = chat_id

        hero_level = HeroLevelDTOModel(
            id=1,
            title='Level',
            order=1,
            need_experience=0,
            count_sentences=0,
            count_games=0,
        )

        telegram_user_model = TelegramUserDTOModel(
            telegram_id=chat_id,
            user_name='UserName',
            experience=10,
            previous_stage='PreviousStage',
            stage='CurrentStage',
            main_language=None,
            level_en=None,
            hero_level=hero_level,
        )

        self._state.get_data = AsyncMock(return_value={'telegram_user': telegram_user_model})

        self._service = WaitNameService(message=self._message, state=self._state)
        self._service._telegram_user = telegram_user_model

        await self._service._update_name_for_old_client()

        mock_update_profile.assert_not_awaited()

        expected_data_for_update_user = {
            'telegram_id': chat_id,
            'user_name': 'Newname',
            'stage': State.update_profile.value,
        }

        mock_update_user.assert_awaited_once_with(
            telegram_id=chat_id,
            params_for_update=expected_data_for_update_user,
            url_for_update=f'telegram_user/{chat_id}',
        )

    @mark.asyncio
    async def test_get_message_text_new_client(self):
        self._service = WaitNameService(message=self._message, state=self._state)
        self._service._update_name_for_new_client = AsyncMock()
        self._service._update_name_for_old_client = AsyncMock()

        self._service._telegram_user = TelegramUserDTOModel(
            telegram_id=12345,
            user_name='UserName',
            experience=10,
            previous_stage=State.new_client.value,
            stage='CurrentStage',
            main_language=None,
            level_en=None,
            hero_level=None,
        )

        await self._service._get_message_text()

        self._service._update_name_for_new_client.assert_called_once()
        self._service._update_name_for_old_client.assert_not_called()

    @mark.asyncio
    async def test_get_message_text_old_client(self):
        self._service = WaitNameService(message=self._message, state=self._state)
        self._service._update_name_for_new_client = AsyncMock()
        self._service._update_name_for_old_client = AsyncMock()

        self._service._telegram_user = TelegramUserDTOModel(
            telegram_id=12345,
            user_name='UserName',
            experience=10,
            previous_stage='',
            stage='CurrentStage',
            main_language=None,
            level_en=None,
            hero_level=None,
        )

        await self._service._get_message_text()

        self._service._update_name_for_new_client.assert_not_called()
        self._service._update_name_for_old_client.assert_called_once()
