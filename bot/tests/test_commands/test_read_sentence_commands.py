
from unittest.mock import AsyncMock, patch, call, ANY, mock_open

from aiogram.types import CallbackQuery, Message, ParseMode, ReplyKeyboardMarkup, KeyboardButton, User, ReplyKeyboardRemove
from pytest import mark

from bot import bot
from choices import State
from commands import handle_read_sentence, handle_read_sentence_other_data, handle_end_read_sentence_today
from tests.fixtures import *


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

    @mark.parametrize('is_update_sentence, user_level_en', [(True, 1), (True, 2), (True, 3), (True, 4), (True, 5), (True, 6), (False, 1), (False, 6)])
    @patch('commands.read_sentence.delete_message')
    @patch('commands.read_sentence.update_data_by_api')
    @patch('commands.read_sentence.bot', new_callable=AsyncMock)
    @patch('commands.read_sentence.randint')
    @mark.asyncio
    async def test_handle_just_read_sentence(
            self, mock_randint, mock_bot, mock_update_data, mock_delete_message, is_update_sentence, user_level_en, telegram_user_with_sentence_and_word):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name='Test User')
        mock_callback = CallbackQuery(id=1, chat=chat_id, data='other_data', from_user=user, message=Message(id=1))
        mock_callback.from_user = user
        state = AsyncMock()
        telegram_user = telegram_user_with_sentence_and_word
        telegram_user.level_en.order = user_level_en
        state.get_data = AsyncMock(return_value={'user': telegram_user})
        mock_randint.side_effect = [3, 6]

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
            sentence_text = telegram_user.new_sentence.text
            if telegram_user.level_en.order < 3:
                sentence_text = telegram_user.new_sentence.text_with_words
            expected_message_text = (f'{sentence_text}\n\n'
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

    @patch('os.path.isfile')
    @patch('commands.read_sentence.delete_message')
    @patch('commands.read_sentence.update_data_by_api')
    @patch('commands.read_sentence.bot', new_callable=AsyncMock)
    @patch('commands.read_sentence.randint')
    @mark.asyncio
    async def test_handle_read_sentence_with_audio(
            self, mock_randint, mock_bot, mock_update_data, mock_delete_message, mock_is_file, telegram_user_with_sentence_and_word):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name='Test User')
        mock_callback = CallbackQuery(id=1, chat=chat_id, data='other_data', from_user=user, message=Message(id=1))
        mock_callback.from_user = user
        state = AsyncMock()
        telegram_user = telegram_user_with_sentence_and_word
        telegram_user.level_en.order = 1
        state.get_data = AsyncMock(return_value={'user': telegram_user})
        mock_randint.side_effect = [1, 6]
        mock_update_data.return_value = True
        mock_is_file.return_value = True
        mock_audio_file = mock_open(read_data=b"audio file content")
        with patch('builtins.open', mock_audio_file):
            await handle_read_sentence(message=mock_callback, state=state)

            mock_update_data.assert_called_once_with(
                telegram_id=chat_id,
                params_for_update={'id': state.get_data.return_value['user'].new_sentence.history_sentence_id, 'is_read': True},
                url_for_update=f'history/sentences/{state.get_data.return_value["user"].new_sentence.history_sentence_id}',
            )

            sentence_text = telegram_user.new_sentence.text
            if telegram_user.level_en.order < 3:
                sentence_text = telegram_user.new_sentence.text_with_words
            expected_message_text = f'Text:\n\n<tg-spoiler>{sentence_text}</tg-spoiler>'
            expected_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            expected_keyboard.add(KeyboardButton(text='Read'))
            mock_bot.send_audio.assert_called_once_with(
                chat_id=chat_id,
                audio=ANY,
                caption=expected_message_text,
                parse_mode=ParseMode.HTML,
                reply_markup=expected_keyboard,
            )

            mock_bot.send_message.assert_called_once_with(
                chat_id=chat_id,
                text=f'Translate:\n\n<tg-spoiler>{telegram_user.new_sentence.translation.get("ru")}</tg-spoiler>',
                parse_mode=ParseMode.HTML,
                reply_markup=expected_keyboard,
            )

            mock_delete_message.assert_called_once_with(message=mock_callback)

    @patch('commands.read_sentence.update_data_by_api')
    @patch('commands.read_sentence.bot', new_callable=AsyncMock)
    @patch('commands.read_sentence.randint')
    @mark.asyncio
    async def test_handle_read_sentence_question_about_time(
            self, mock_randint, mock_bot, mock_update_data, telegram_user_with_sentence_and_word):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name='Test User')
        mock_callback = CallbackQuery(id=1, chat=chat_id, data='other_data', from_user=user, message=Message(id=1))
        mock_callback.from_user = user
        state = AsyncMock()
        telegram_user = telegram_user_with_sentence_and_word
        state.get_data = AsyncMock(return_value={'user': telegram_user})
        mock_randint.side_effect = [3, 1, 50, 20, 20, 20]

        mock_update_data.return_value = True

        await handle_read_sentence(message=mock_callback, state=state)
        mock_update_data.assert_called_once_with(
            telegram_id=chat_id,
            params_for_update={'stage': State.check_answer_time.value, 'telegram_id': telegram_user.telegram_id},
            url_for_update=f'telegram_user/{telegram_user.telegram_id}',
        )

        sentence_text = telegram_user.new_sentence.text
        if telegram_user.level_en.order < 3:
            sentence_text = telegram_user.new_sentence.text_with_words
        expected_message_text = (f'{sentence_text}\n\n'
                                 f'<tg-spoiler>{telegram_user.new_sentence.translation.get("ru")}</tg-spoiler>')
        expected_keyboard = ReplyKeyboardRemove()
        assert mock_bot.send_message.call_args_list[0] == call(
            chat_id=chat_id,
            text=expected_message_text,
            parse_mode=ParseMode.HTML,
            reply_markup=expected_keyboard,
        )

        expected_message_text = 'К какому времени относится предложение?'
        assert mock_bot.send_message.call_args_list[1] == call(
            chat_id=chat_id,
            text=expected_message_text,
            parse_mode=ParseMode.HTML,
            reply_markup=ANY,
        )



    @patch('commands.read_sentence.delete_message')
    @mark.asyncio
    async def test_handle_end_read_sentence_today_message(self, mock_delete_message):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name='Test User')
        mock_message = Message(id=1, chat=chat_id, text='Read', from_user=user)
        mock_message.from_user = user

        with patch.object(bot, 'send_message', new=AsyncMock()) as mock_send_message:
            await handle_end_read_sentence_today(mock_message)
            expected_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            expected_keyboard.add(KeyboardButton(text='Read'))
            expected_text = 'Вы прочитали все предложения на сегодня. Приходите завтра.'
            mock_send_message.assert_called_once_with(chat_id=chat_id, text=expected_text, reply_markup=expected_keyboard, parse_mode=ParseMode.HTML)
            mock_delete_message.assert_called_once_with(message=mock_message)

    @patch('commands.read_sentence.delete_message')
    @mark.asyncio
    async def test_handle_end_read_sentence_today_callback(self, mock_delete_message):
        chat_id = 1
        user = User(id=chat_id, is_bot=False, first_name='Test User')
        mock_callback = CallbackQuery(id=1, chat=chat_id, data='other_data', from_user=user)
        mock_callback.from_user = user

        with patch.object(bot, 'send_message', new=AsyncMock()) as mock_send_message:
            await handle_end_read_sentence_today(mock_callback)
            expected_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            expected_keyboard.add(KeyboardButton(text='Read'))
            expected_text = 'Вы прочитали все предложения на сегодня. Приходите завтра.'
            mock_send_message.assert_called_once_with(chat_id=chat_id, text=expected_text, reply_markup=expected_keyboard, parse_mode=ParseMode.HTML)
            mock_delete_message.assert_called_once_with(message=mock_callback)
