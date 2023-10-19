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

    @mark.asyncio
    async def test_update_en_level_for_old_client(self):
        chat_id = 12345
        start_message_text = '🤖 Уровень английского изменён.\n'
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

        update_profile_service_do_mock = AsyncMock()
        with patch.object(UpdateProfileService, 'do', update_profile_service_do_mock):
            await self._service._update_en_level_for_old_client()

        assert self._service._stage == State.update_profile.value
        assert self._service._start_message_text == start_message_text
        assert self._service._chat_id == chat_id

        self._service._update_user.assert_awaited_once()

        update_profile_service_do_mock.assert_awaited_once()

    @mark.asyncio
    async def test_update_en_level_for_old_client_with_mistake(self):
        chat_id = 12345
        self._callback.data = 'level_en_1'
        self._callback.from_user.id = chat_id
        self._service = WaitEnLevelService(callback_query=self._callback, state=self._state)
        self._service._update_user = AsyncMock(return_value=False)

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

        update_profile_service_do_mock = AsyncMock()
        with patch.object(UpdateProfileService, 'do', update_profile_service_do_mock):
            await self._service._update_en_level_for_old_client()

        assert self._service._stage == State.update_profile.value
        assert self._service._chat_id == chat_id
        assert not hasattr(self._service, '_start_message_text')

        self._service._update_user.assert_awaited_once()

        update_profile_service_do_mock.assert_not_awaited()

    @mark.asyncio
    async def test_update_en_level_for_new_client(self):
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

    @mark.asyncio
    async def test_update_en_level_for_new_client_with_mistake(self):
        chat_id = 12345
        self._callback.data = 'level_en_1'
        self._callback.from_user.id = chat_id
        self._service = WaitEnLevelService(callback_query=self._callback, state=self._state)
        self._service._update_user = AsyncMock(return_value=False)

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

    @mark.parametrize('english_level_id, callback_data', [
        (1, 'level_en_1'), (2, 'level_en_2'), (3, 'level_en_3'), (4, 'level_en_4'), (5, 'level_en_5'), (6, 'level_en_6')
    ])
    @mark.asyncio
    async def test_update_user(self, mocker, english_level_id, callback_data):
        chat_id = 12345
        self._callback.data = callback_data
        self._callback.from_user.id = chat_id
        self._service = WaitEnLevelService(callback_query=self._callback, state=self._state)

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

        self._service._telegram_user = telegram_user_model
        self._service._stage = 'Stage'
        self._service._previous_stage = 'CurrentStage'

        with patch('context_managers.aio_http_client.AsyncHttpClient.patch', return_value=({}, HTTPStatus.OK)) as mocked_post:
            return_value = await self._service._update_user()

        mocked_post.assert_awaited_once_with(
            url=f'{settings.api_url}/v1/telegram_user/{telegram_user_model.telegram_id}',
            headers=settings.api_headers,
            json={
                'telegram_id': telegram_user_model.telegram_id,
                'level_en_id': english_level_id,
                'stage': 'Stage',
                'previous_stage': 'CurrentStage',
            }
        )

        assert return_value is True

    @mark.asyncio
    async def test_update_user_with_mistake(self, mocker):
        chat_id = 12345
        self._callback.data = 'level_en_1'
        self._callback.from_user.id = chat_id
        self._service = WaitEnLevelService(callback_query=self._callback, state=self._state)

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

        self._service._telegram_user = telegram_user_model
        self._service._stage = 'Stage'
        self._service._previous_stage = 'CurrentStage'

        with patch('context_managers.aio_http_client.AsyncHttpClient.patch', return_value=({}, HTTPStatus.NOT_FOUND)) as mocked_post:
            with patch.object(bot, 'send_message', new=AsyncMock()) as mock_send_message:
                return_value = await self._service._update_user()

        mocked_post.assert_awaited_once_with(
            url=f'{settings.api_url}/v1/telegram_user/{telegram_user_model.telegram_id}',
            headers=settings.api_headers,
            json={
                'telegram_id': telegram_user_model.telegram_id,
                'level_en_id': 1,
                'stage': 'Stage',
                'previous_stage': 'CurrentStage',
            }
        )

        assert return_value is False

        expected_calls = [
            call(chat_id=chat_id, text='🤖 Что-то пошло не так. Попробуйте еще раз, чуть позже.'),
        ]
        mock_send_message.assert_has_calls(expected_calls, any_order=True)
