from http import HTTPStatus

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from pytest import mark
from unittest.mock import ANY, AsyncMock, Mock, patch, call

from bot import bot
from choices import State
from dto import TelegramUserDTOModel
from settings import settings
from services import WaitEnLevelService, UpdateProfileService


class TestWaitEnLevelService:
    """Tests for wait en level"""

    @classmethod
    def setup_class(cls):
        cls._callback = Mock()
        cls._post_method_target = 'context_managers.aio_http_client.AsyncHttpClient.post'
        cls._state = Mock()

    @mark.asyncio
    async def test_get_user(self, mocker):
        """Test get user."""

        self._callback.from_user.id = 12345
        self._callback.data = 'level_en_1'

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
        self._state.get_data = AsyncMock(return_value={'user': telegram_user_model})

        self._service = WaitEnLevelService(callback_query=self._callback, state=self._state)

        await self._service._get_user()
        assert self._service._telegram_user == telegram_user_model
        self._state.get_data.assert_awaited_once()

    @mark.asyncio
    async def test_get_message_text_new_client(self):
        self._callback.data = 'level_en_1'
        self._service = WaitEnLevelService(callback_query=self._callback, state=self._state)
        self._service._update_en_level_for_new_client = AsyncMock()
        self._service._update_en_level_for_old_client = AsyncMock()

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

        self._service._update_en_level_for_new_client.assert_called_once()
        self._service._update_en_level_for_old_client.assert_not_called()

    @mark.asyncio
    async def test_get_message_text_old_client(self):
        self._callback.data = 'level_en_1'
        self._service = WaitEnLevelService(callback_query=self._callback, state=self._state)
        self._service._update_en_level_for_new_client = AsyncMock()
        self._service._update_en_level_for_old_client = AsyncMock()

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

        self._service._update_en_level_for_new_client.assert_not_called()
        self._service._update_en_level_for_old_client.assert_called_once()

    @mark.parametrize('english_level_id, callback_data', [
        (1, 'level_en_1'), (2, 'level_en_2'), (3, 'level_en_3'), (4, 'level_en_4'), (5, 'level_en_5'), (6, 'level_en_6')
    ])
    @patch('services.wait_en_level.UpdateProfileService')
    @patch('services.wait_en_level.update_data_by_api', new_callable=AsyncMock)
    @mark.asyncio
    async def test_update_en_level_for_old_client(self, mock_update_user, mock_update_profile, english_level_id, callback_data):
        mock_update_user.side_effect = [True]

        chat_id = 12345
        start_message_text = '🤖 Уровень английского изменён.\n'
        self._callback.data = callback_data
        self._callback.from_user.id = chat_id
        self._service = WaitEnLevelService(callback_query=self._callback, state=self._state)

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

        mock_update_profile.return_value.do = AsyncMock()

        await self._service._update_en_level_for_old_client()

        assert self._service._chat_id == chat_id

        mock_update_profile.assert_called_once_with(chat_id=chat_id, start_message_text=start_message_text)
        mock_update_profile.return_value.do.assert_awaited_once()

        expected_data_for_update_user = {
            'telegram_id': chat_id,
            'level_en_id': english_level_id,
            'stage': State.update_profile.value,
        }

        mock_update_user.assert_awaited_once_with(
            telegram_id=chat_id,
            params_for_update=expected_data_for_update_user,
            url_for_update=f'telegram_user/{chat_id}',
        )

    @patch('services.wait_en_level.UpdateProfileService.do', new_callable=AsyncMock)
    @patch('services.wait_en_level.update_data_by_api', new_callable=AsyncMock)
    @mark.asyncio
    async def test_update_en_level_for_old_client_with_mistake(self, mock_update_user, mock_update_profile):
        mock_update_user.side_effect = [False]
        chat_id = 12345
        self._callback.data = 'level_en_1'
        self._callback.from_user.id = chat_id
        self._service = WaitEnLevelService(callback_query=self._callback, state=self._state)

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

        await self._service._update_en_level_for_old_client()

        mock_update_profile.assert_not_awaited()

        expected_data_for_update_user = {
            'telegram_id': chat_id,
            'level_en_id': 1,
            'stage': State.update_profile.value,
        }

        mock_update_user.assert_awaited_once_with(
            telegram_id=chat_id,
            params_for_update=expected_data_for_update_user,
            url_for_update=f'telegram_user/{chat_id}',
        )

    @patch('services.wait_en_level.update_data_by_api', new_callable=AsyncMock)
    @mark.asyncio
    async def test_update_en_level_for_new_client(self, mock_update_user):
        mock_update_user.side_effect = [True]
        chat_id = 12345
        self._callback.data = 'level_en_1'
        self._callback.from_user.id = chat_id
        self._service = WaitEnLevelService(callback_query=self._callback, state=self._state)
        self._service._update_user = AsyncMock(return_value=True)

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

        with patch.object(bot, 'send_message', new=AsyncMock()) as mock_send_message:
            await self._service._update_en_level_for_new_client()

            expected_calls = [
                call(chat_id=chat_id, text='Поздравляю ты выполнил первое задание на день! Теперь ты можешь прочитать первый рассказ.'),
                call(chat_id=chat_id, text='Теперь ты готов к изучению английского языка. Для начала прочитай первый рассказ.', reply_markup=ANY)
            ]
            mock_send_message.assert_has_calls(expected_calls, any_order=True)

            reply_markup_call = mock_send_message.call_args_list[1]
            reply_markup = reply_markup_call.kwargs['reply_markup']

            assert isinstance(reply_markup, ReplyKeyboardMarkup)
            assert reply_markup.resize_keyboard is True
            assert reply_markup.keyboard == [[KeyboardButton(text='Read')]]

            expected_data_for_update_user = {
                'telegram_id': chat_id,
                'level_en_id': 1,
                'stage': State.read_book.value,
                'previous_stage': '',
            }

            mock_update_user.assert_awaited_once_with(
                telegram_id=chat_id,
                params_for_update=expected_data_for_update_user,
                url_for_update=f'telegram_user/{chat_id}',
            )

    @patch('services.wait_en_level.update_data_by_api', new_callable=AsyncMock)
    @mark.asyncio
    async def test_update_en_level_for_new_client_with_mistake(self, mock_update_user):
        mock_update_user.side_effect = [False]
        chat_id = 12345
        self._callback.data = 'level_en_1'
        self._callback.from_user.id = chat_id
        self._service = WaitEnLevelService(callback_query=self._callback, state=self._state)

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

        with patch.object(bot, 'send_message', new=AsyncMock()) as mock_send_message:
            await self._service._update_en_level_for_new_client()
            mock_send_message.assert_not_awaited()

            expected_data_for_update_user = {
                'telegram_id': chat_id,
                'level_en_id': 1,
                'stage': State.read_book.value,
                'previous_stage': '',
            }

            mock_update_user.assert_awaited_once_with(
                telegram_id=chat_id,
                params_for_update=expected_data_for_update_user,
                url_for_update=f'telegram_user/{chat_id}',
            )
