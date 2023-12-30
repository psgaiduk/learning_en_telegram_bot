from unittest.mock import AsyncMock, patch
from aiogram.types import CallbackQuery, User, ParseMode, ReplyKeyboardMarkup, KeyboardButton
from pytest import mark

from choices import State
from commands import handle_check_answer_time
from tests.fixtures import *


class TestCheckAnswerTime:
    """Tests command check answer time."""

    @mark.parametrize('data', ['right_answer_time', 'wrong_answer_time'])
    @patch('commands.check_answer_time.delete_message')
    @patch('commands.check_answer_time.update_data_by_api')
    @patch('commands.check_answer_time.bot', new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_check_answer_time(
            self, mock_bot, mock_update_data, mock_delete_message, data, telegram_user_with_sentence_and_word):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name='Test User')
        mock_callback = CallbackQuery(id=1, chat=chat_id, data=data, from_user=user)
        mock_callback.from_user = user
        state = AsyncMock()
        telegram_user = telegram_user_with_sentence_and_word
        state.get_data = AsyncMock(return_value={'user': telegram_user})
        mock_update_data.side_effect = [True, True]

        await handle_check_answer_time(message=mock_callback, state=state)

        mock_update_data.assert_any_call(
            telegram_id=chat_id,
            params_for_update={'id': telegram_user.new_sentence.history_sentence_id, 'is_read': True},
            url_for_update=f'history/sentences/{telegram_user.new_sentence.history_sentence_id}',
        )

        mock_update_data.assert_any_call(
            telegram_id=chat_id,
            params_for_update={'telegram_id': chat_id, 'stage': State.read_book.value},
            url_for_update=f'telegram_user/{chat_id}',
        )

        start_expected_message_text = f'Правильный ответ: {telegram_user.new_sentence.sentence_times}'
        if data == 'right_answer_time':
            start_expected_message_text = f'Правильно.!'

        expected_message_text = f'{start_expected_message_text}\n\n{telegram_user.new_sentence.description_time}'
        expected_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        expected_keyboard.add(KeyboardButton(text='Read'))
        mock_bot.send_message.assert_called_once_with(
            chat_id=chat_id,
            text=expected_message_text,
            parse_mode=ParseMode.HTML,
            reply_markup=expected_keyboard,
        )

        mock_delete_message.assert_called_once_with(message=mock_callback)

    @mark.parametrize('data', ['right_answer_time', 'wrong_answer_time'])
    @patch('commands.check_answer_time.delete_message')
    @patch('commands.check_answer_time.update_data_by_api')
    @patch('commands.check_answer_time.bot', new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_check_answer_time_mistake_update_user(
            self, mock_bot, mock_update_data, mock_delete_message, data, telegram_user_with_sentence_and_word):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name='Test User')
        mock_callback = CallbackQuery(id=1, chat=chat_id, data=data, from_user=user)
        mock_callback.from_user = user
        state = AsyncMock()
        telegram_user = telegram_user_with_sentence_and_word
        state.get_data = AsyncMock(return_value={'user': telegram_user})
        mock_update_data.side_effect = [True, False]

        await handle_check_answer_time(message=mock_callback, state=state)

        mock_update_data.assert_any_call(
            telegram_id=chat_id,
            params_for_update={'id': telegram_user.new_sentence.history_sentence_id, 'is_read': True},
            url_for_update=f'history/sentences/{telegram_user.new_sentence.history_sentence_id}',
        )

        mock_update_data.assert_any_call(
            telegram_id=chat_id,
            params_for_update={'telegram_id': chat_id, 'stage': State.read_book.value},
            url_for_update=f'telegram_user/{chat_id}',
        )

        mock_bot.send_message.assert_not_called()
        mock_delete_message.assert_not_called()

    @mark.parametrize('data', ['right_answer_time', 'wrong_answer_time'])
    @patch('commands.check_answer_time.delete_message')
    @patch('commands.check_answer_time.update_data_by_api')
    @patch('commands.check_answer_time.bot', new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_check_answer_time_mistake_update_sentence(
            self, mock_bot, mock_update_data, mock_delete_message, data, telegram_user_with_sentence_and_word):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name='Test User')
        mock_callback = CallbackQuery(id=1, chat=chat_id, data=data, from_user=user)
        mock_callback.from_user = user
        state = AsyncMock()
        telegram_user = telegram_user_with_sentence_and_word
        state.get_data = AsyncMock(return_value={'user': telegram_user})
        mock_update_data.side_effect = [False]

        await handle_check_answer_time(message=mock_callback, state=state)

        mock_update_data.assert_called_once_with(
            telegram_id=chat_id,
            params_for_update={'id': telegram_user.new_sentence.history_sentence_id, 'is_read': True},
            url_for_update=f'history/sentences/{telegram_user.new_sentence.history_sentence_id}',
        )

        mock_bot.send_message.assert_not_called()
        mock_delete_message.assert_not_called()
