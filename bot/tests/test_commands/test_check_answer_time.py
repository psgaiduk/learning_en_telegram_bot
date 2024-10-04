from unittest.mock import AsyncMock, patch
from aiogram.types import CallbackQuery, KeyboardButton, ParseMode, ReplyKeyboardMarkup, User
from pytest import fixture, mark

from choices import State
from commands import handle_check_answer_time, handle_check_answer_time_other_data
from tests.fixtures import *


class TestCheckAnswerTime:
    """Tests command check answer time."""

    @fixture(autouse=True)
    def setup_method(self, telegram_user_with_sentence_and_word):
        self._chat_id = 1
        self._user = User(id=self._chat_id, is_bot=False, first_name='Test User')
        self._mock_callback = CallbackQuery(id=1, chat=self._chat_id, from_user=self._user)
        self._mock_callback.from_user = self._user
        self._telegram_user = telegram_user_with_sentence_and_word
        self._state = AsyncMock()
        self._state.get_data = AsyncMock(return_value={'telegram_user': self._telegram_user})

    @mark.parametrize('data', ['right_answer_time', 'wrong_answer_time'])
    @patch('commands.check_answer_time.delete_message')
    @patch('commands.check_answer_time.update_data_by_api')
    @patch('commands.check_answer_time.bot', new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_check_answer_time(self, mock_bot, mock_update_data, mock_delete_message, data):
        self._mock_callback.data = data
        mock_update_data.side_effect = [True, True]

        await handle_check_answer_time(message=self._mock_callback, state=self._state)

        mock_update_data.assert_any_call(
            telegram_id=self._chat_id,
            params_for_update={'id': self._telegram_user.new_sentence.history_sentence_id, 'is_read': True},
            url_for_update=f'history/sentences/{self._telegram_user.new_sentence.history_sentence_id}',
        )

        mock_update_data.assert_any_call(
            telegram_id=self._chat_id,
            params_for_update={'telegram_id': self._chat_id, 'stage': State.start_learn_words.value},
            url_for_update=f'telegram_user/{self._chat_id}',
        )

        start_expected_message_text = f'Правильный ответ: {self._telegram_user.new_sentence.sentence_times}'
        if data == 'right_answer_time':
            start_expected_message_text = f'Правильно.!'

        expected_message_text = f'{start_expected_message_text}\n\n{self._telegram_user.new_sentence.description_time}'
        expected_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        expected_keyboard.add(KeyboardButton(text='Read'))
        mock_bot.send_message.assert_called_once_with(
            chat_id=self._chat_id,
            text=expected_message_text,
            parse_mode=ParseMode.HTML,
            reply_markup=expected_keyboard,
        )

        mock_delete_message.assert_called_once_with(message=self._mock_callback, state=self._state)

    @mark.parametrize('data', ['right_answer_time', 'wrong_answer_time'])
    @patch('commands.check_answer_time.delete_message')
    @patch('commands.check_answer_time.update_data_by_api')
    @patch('commands.check_answer_time.bot', new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_check_answer_time_mistake_update_user(self, mock_bot, mock_update_data, mock_delete_message, data):
        mock_update_data.side_effect = [True, False]

        await handle_check_answer_time(message=self._mock_callback, state=self._state)

        mock_update_data.assert_any_call(
            telegram_id=self._chat_id,
            params_for_update={'id': self._telegram_user.new_sentence.history_sentence_id, 'is_read': True},
            url_for_update=f'history/sentences/{self._telegram_user.new_sentence.history_sentence_id}',
        )

        mock_update_data.assert_any_call(
            telegram_id=self._chat_id,
            params_for_update={'telegram_id': self._chat_id, 'stage': State.start_learn_words.value},
            url_for_update=f'telegram_user/{self._chat_id}',
        )

        mock_bot.send_message.assert_not_called()
        mock_delete_message.assert_not_called()

    @mark.parametrize('data', ['right_answer_time', 'wrong_answer_time'])
    @patch('commands.check_answer_time.delete_message')
    @patch('commands.check_answer_time.update_data_by_api')
    @patch('commands.check_answer_time.bot', new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_check_answer_time_mistake_update_sentence(self, mock_bot, mock_update_data, mock_delete_message, data):
        mock_update_data.side_effect = [False]

        await handle_check_answer_time(message=self._mock_callback, state=self._state)

        mock_update_data.assert_called_once_with(
            telegram_id=self._chat_id,
            params_for_update={'id': self._telegram_user.new_sentence.history_sentence_id, 'is_read': True},
            url_for_update=f'history/sentences/{self._telegram_user.new_sentence.history_sentence_id}',
        )

        mock_bot.send_message.assert_not_called()
        mock_delete_message.assert_not_called()

    @patch('commands.check_answer_time.bot', new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_check_answer_time_other_data(self, mock_bot,):
        await handle_check_answer_time_other_data(message=self._mock_callback)

        expected_message_text = 'Нужно нажать по кнопке со временем предложения.'
        mock_bot.send_message.assert_called_once_with(
            chat_id=self._chat_id,
            text=expected_message_text,
            parse_mode=ParseMode.HTML,
        )
