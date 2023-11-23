from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytest import mark
from unittest.mock import ANY, AsyncMock, patch

from bot import bot
from choices import State
from dto import TelegramUserDTOModel, NewSentenceDTOModel, WordDTOModel
from services import CheckWordsService


class TestCheckWordsService:
    """Tests for CheckWordsService."""

    def setup_method(self):
        self._state = AsyncMock()
        self._chat_id = 12345
        self._word = WordDTOModel(
                    word_id=1,
                    word='test_word',
                    type_word_id=1,
                    translation={'ru': 'test_word'},
                    is_known=False,
                    count_view=0,
                    correct_answers=0,
                    incorrect_answers=0,
                    correct_answers_in_row=0,
                )
        self._new_sentence = NewSentenceDTOModel(
            history_sentence_id=1,
            book_id=1,
            sentence_id=1,
            text='test_text',
            translation={'ru': 'test_text'},
            words=[self._word],
        )
        self._telegram_user = TelegramUserDTOModel(
            stage='test_stage',
            user_name='test_name',
            experience=0,
            previous_stage='test_previous_stage',
            telegram_id=self._chat_id,
            hero_level=None,
            level_en=None,
            main_language=None,
            new_sentence=self._new_sentence,
        )

    @mark.asyncio
    async def test_do_all_true(self):
        service = CheckWordsService(state=self._state, start_text_message='')
        
        mock_get_user = AsyncMock(return_value=None)
        service._get_user = mock_get_user
        service._telegram_user = self._telegram_user

        mock_update_user = AsyncMock(return_value=True)
        service._update_user = mock_update_user

        mock_update_sentence = AsyncMock(return_value=True)
        service._update_sentence = mock_update_sentence

        mock_send_message = AsyncMock(return_value=None)
        service._send_message = mock_send_message
        
        await service.do()

        mock_get_user.assert_called_once()
        mock_update_user.assert_called_once()
        mock_update_sentence.assert_called_once()
        mock_send_message.assert_called_once()

        assert service._words == []
        assert service._first_word == self._word

    @mark.asyncio
    async def test_do_update_user_false(self):
        service = CheckWordsService(state=self._state, start_text_message='')

        mock_get_user = AsyncMock(return_value=None)
        service._get_user = mock_get_user
        service._telegram_user = self._telegram_user

        mock_update_user = AsyncMock(return_value=False)
        service._update_user = mock_update_user

        mock_update_sentence = AsyncMock(return_value=True)
        service._update_sentence = mock_update_sentence

        mock_send_message = AsyncMock(return_value=None)
        service._send_message = mock_send_message

        await service.do()

        mock_get_user.assert_called_once()
        mock_update_user.assert_called_once()
        mock_update_sentence.assert_not_called()
        mock_send_message.assert_not_called()

    @mark.asyncio
    async def test_do_update_sentence_false(self):
        service = CheckWordsService(state=self._state, start_text_message='')

        mock_get_user = AsyncMock(return_value=None)
        service._get_user = mock_get_user
        service._telegram_user = self._telegram_user

        mock_update_user = AsyncMock(return_value=True)
        service._update_user = mock_update_user

        mock_update_sentence = AsyncMock(return_value=False)
        service._update_sentence = mock_update_sentence

        mock_send_message = AsyncMock(return_value=None)
        service._send_message = mock_send_message

        await service.do()

        mock_get_user.assert_called_once()
        mock_update_user.assert_called_once()
        mock_update_sentence.assert_called_once()
        mock_send_message.assert_not_called()
    
    @mark.asyncio
    async def test_get_user(self):
        service = CheckWordsService(state=self._state, start_text_message='')

        self._state.get_data = AsyncMock(return_value={'user': self._telegram_user})

        await service._get_user()

        assert service._telegram_user == self._telegram_user

    @mark.parametrize('update_status', [True, False])
    @mark.asyncio
    @patch('services.check_words.update_data_by_api', new_callable=AsyncMock)
    async def test_update_user(self, mock_update_user, update_status):
        service = CheckWordsService(state=self._state, start_text_message='')
        service._telegram_user = self._telegram_user

        mock_update_user.side_effect = [update_status]

        return_value = await service._update_user()

        mock_update_user.assert_called_once_with(
            telegram_id=self._telegram_user.telegram_id,
            params_for_update={
                'telegram_id': self._telegram_user.telegram_id,
                'stage': State.read_book.value,
            },
            url_for_update=f'telegram_user/{self._telegram_user.telegram_id}',
        )

        assert return_value is update_status

    @mark.parametrize('update_status', [True, False])
    @mark.asyncio
    @patch('services.check_words.update_data_by_api', new_callable=AsyncMock)
    async def test_update_sentence(self, mock_update_user, update_status):
        service = CheckWordsService(state=self._state, start_text_message='')
        service._telegram_user = self._telegram_user
        service._words = self._new_sentence.words

        mock_update_user.side_effect = [update_status]

        return_value = await service._update_sentence()

        words_ids = [word.word_id for word in self._new_sentence.words]

        mock_update_user.assert_called_once_with(
            telegram_id=self._telegram_user.telegram_id,
            params_for_update={
                'id': self._telegram_user.new_sentence.history_sentence_id,
                'check_words': words_ids,
            },
            url_for_update=f'history/sentences/{self._telegram_user.new_sentence.history_sentence_id}',
        )

        assert return_value is update_status

    @mark.parametrize('start_message_text', ['', 'Text', 'Another text'])
    @mark.asyncio
    async def test_send_message(self, start_message_text):
        service = CheckWordsService(state=self._state, start_text_message='')
        service._telegram_user = self._telegram_user
        service._first_word = self._word
        service._start_text_message = start_message_text

        with patch.object(bot, 'send_message', new=AsyncMock()) as mock_send_message:
            await service._send_message()

            excepted_text = f'{start_message_text}Слово: {self._word.word}\nПеревод: {self._word.translation["ru"]}'

            mock_send_message.assert_called_once_with(
                chat_id=self._chat_id,
                text=excepted_text,
                reply_markup=ANY,
            )

            reply_markup_call = mock_send_message.call_args_list[0]
            reply_markup = reply_markup_call.kwargs['reply_markup']

            assert isinstance(reply_markup, InlineKeyboardMarkup)
            assert reply_markup.inline_keyboard == [
                [InlineKeyboardButton(text='I know', callback_data=f'know_word_true_{self._word.word_id}')],
                [InlineKeyboardButton(text='I don\'t know', callback_data=f'know_word_false_{self._word.word_id}')],
            ]
