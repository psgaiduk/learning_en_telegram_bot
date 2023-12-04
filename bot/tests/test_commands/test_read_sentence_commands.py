from unittest.mock import AsyncMock, patch

from aiogram.types import CallbackQuery, Message, ParseMode, ReplyKeyboardMarkup, KeyboardButton, User
from pytest import mark

from bot import bot
from commands import handle_read_sentence, handle_read_sentence_other_data
from tests.fixtures import telegram_user_with_sentence_and_word, sentence_with_word, word_new


class TestReadSentenceCommand:
    """Tests command read sentence."""

    @mark.asyncio
    async def test_handle_read_sentence_other_data_callback(self):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name='Test User')
        mock_callback = CallbackQuery(id=1, chat=chat_id, data='other_data', from_user=user)
        mock_callback.from_user = user

        with patch.object(bot, 'send_message', new=AsyncMock()) as mock_send_message:
            await handle_read_sentence_other_data(mock_callback)
            expected_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            expected_keyboard.add(KeyboardButton(text='Read'))
            expected_text = 'Нужно нажать по кнопке Read'
            mock_send_message.assert_called_once_with(chat_id=chat_id, text=expected_text, reply_markup=expected_keyboard, parse_mode=ParseMode.HTML)

    @mark.asyncio
    async def test_handle_read_sentence_other_data_message(self):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name='Test User')
        mock_message = Message(id=1, chat=chat_id, text='Read', from_user=user)
        mock_message.from_user = user

        with patch.object(bot, 'send_message', new=AsyncMock()) as mock_send_message:
            await handle_read_sentence_other_data(mock_message)
            expected_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            expected_keyboard.add(KeyboardButton(text='Read'))
            expected_text = 'Нужно нажать по кнопке Read'
            mock_send_message.assert_called_once_with(chat_id=chat_id, text=expected_text, reply_markup=expected_keyboard, parse_mode=ParseMode.HTML)

    @mark.parametrize('is_update_sentence', [True, False])
    @patch('commands.read_sentence.delete_message')
    @patch('commands.read_sentence.update_data_by_api')
    @patch('commands.read_sentence.bot', new_callable=AsyncMock)
    @mark.asyncio
    async def test_handle_read_sentence(
            self, mock_bot, mock_update_data, mock_delete_message, is_update_sentence, telegram_user_with_sentence_and_word):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name='Test User')
        mock_callback = CallbackQuery(id=1, chat=chat_id, data='other_data', from_user=user, message=Message(id=1))
        mock_callback.from_user = user
        state = AsyncMock()
        telegram_user = telegram_user_with_sentence_and_word
        state.get_data = AsyncMock(return_value={'user': telegram_user})

        mock_update_data.return_value = is_update_sentence

        await handle_read_sentence(message=mock_callback, state=state)
        mock_update_data.assert_called_once_with(
            telegram_id=chat_id,
            params_for_update={'id': state.get_data.return_value['user'].new_sentence.history_sentence_id, 'is_read': True},
            url_for_update=f'history/sentences/{state.get_data.return_value["user"].new_sentence.history_sentence_id}',
        )

        if is_update_sentence is False:
            mock_bot.send_message.assert_not_called()
            mock_delete_message.assert_not_called()
        else:
            expected_message_text = (f'{telegram_user.new_sentence.text}\n\n'
                                     f'<tg-spoiler>{telegram_user.new_sentence.translation.get("ru")}</tg-spoiler>')
            expected_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            expected_keyboard.add(KeyboardButton(text='Read'))
            mock_bot.send_message.assert_called_once_with(
                chat_id=chat_id,
                text=expected_message_text,
                parse_mode=ParseMode.HTML,
                reply_markup=expected_keyboard,
            )
            mock_delete_message.assert_called_once_with(message=mock_callback)
