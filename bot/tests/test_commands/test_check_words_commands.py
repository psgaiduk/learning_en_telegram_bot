from unittest.mock import AsyncMock, MagicMock, patch

from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, User
from pytest import mark

from bot import bot
from choices import State
from commands import handle_check_words_other_data, handle_check_words_after_read, handle_check_word_click_known


class TestCheckWordsCommand:
    """Tests command check words."""

    @mark.asyncio
    async def test_handle_check_words_other_data_callback(self, monkeypatch):
        chat_id = 1
        monkeypatch.setattr('commands.check_words.State', MagicMock(value=State.check_words.value))
        user = User(id=chat_id, is_bot=False, first_name="Test User")
        mock_callback = CallbackQuery(id=1, chat=chat_id, data='other_data', from_user=user)
        mock_callback.from_user = user

        with patch.object(bot, 'send_message', new=AsyncMock()) as mock_send_message:
            await handle_check_words_other_data(mock_callback)

            expected_text = 'Нужно нажать по кнопке I know или I don\'t know'

            mock_send_message.assert_called_once_with(chat_id=chat_id, text=expected_text)

    @mark.asyncio
    async def test_handle_check_words_other_data_message(self, monkeypatch):
        chat_id = 1
        monkeypatch.setattr('commands.check_words.State', MagicMock(value=State.check_words.value))
        user = User(id=chat_id, is_bot=False, first_name="Test User")
        mock_message = Message(id=1, chat=chat_id, data='other_data', from_user=user)
        mock_message.from_user = user

        with patch.object(bot, 'send_message', new=AsyncMock()) as mock_send_message:
            await handle_check_words_other_data(mock_message)

            expected_text = 'Нужно нажать по кнопке I know или I don\'t know'

            mock_send_message.assert_called_once_with(chat_id=chat_id, text=expected_text)

    @patch('commands.check_words.delete_message')
    @patch('commands.check_words.send_message_and_delete')
    @patch('commands.check_words.CheckWordsService')
    @mark.asyncio
    async def test_handle_check_words_after_read(self, mock_check_word_service, mock_send_delete_message, mock_delete_message):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name='Test User')
        mock_message = Message(id=1, chat=chat_id, text='Read', from_user=user)
        mock_message.from_user = user
        state = AsyncMock()
        mock_check_word_service.return_value.do = AsyncMock()

        await handle_check_words_after_read(message=mock_message, state=state)

        expected_message_text = 'Прежде чем начать изучать предложение, давай посмотрим слова, которые нам встретятся в этом предложении.\n\n'
        mock_send_delete_message.assert_called_once_with(chat_id=chat_id, message_text=expected_message_text, reply_markup=ReplyKeyboardRemove())
        mock_check_word_service.assert_called_once_with(state=state, start_text_message='')
        mock_check_word_service.return_value.do.assert_awaited_once_with()
        mock_delete_message.assert_called_once_with(message=mock_message)

    @mark.parametrize('callback_data, is_update_history, start_text', [
        ('know_word_true_1', True, 'Отлично! Больше мы его тебе не будем показывать. Давай продолжим.\n\n'),
        ('know_word_false_1', True, 'Хорошо. Повторим потом ещё раз.\n\n'),
        ('know_word_true_1', False, ''),
        ('know_word_false_1', False, ''),
    ])
    @patch('commands.check_words.delete_message')
    @patch('commands.check_words.save_word_history')
    @patch('commands.check_words.CheckWordsService')
    @mark.asyncio
    async def test_handle_check_word_click_known(
            self,
            mock_check_word_service,
            mock_save_word_history,
            mock_delete_message,
            callback_data,
            is_update_history,
            start_text,
    ):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name='Test User')
        message = Message(id=1, chat=chat_id, text='Read', from_user=user)
        mock_callback = CallbackQuery(id=1, chat=chat_id, data=callback_data, from_user=user, message=message)
        mock_callback.from_user = user
        state = AsyncMock()
        mock_check_word_service.return_value.do = AsyncMock()
        mock_save_word_history.return_value = is_update_history, start_text

        await handle_check_word_click_known(callback_query=mock_callback, state=state)

        if is_update_history is True:

            mock_check_word_service.assert_called_once_with(state=state, start_text_message=start_text)
            mock_check_word_service.return_value.do.assert_awaited_once_with()
            mock_delete_message.assert_called_once_with(message=mock_callback)
        else:
            mock_check_word_service.assert_not_called()
            mock_delete_message.assert_not_called()
