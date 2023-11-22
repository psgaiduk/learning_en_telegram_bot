from http import HTTPStatus

from aiohttp import ClientResponse
from pytest import mark
from unittest.mock import AsyncMock, Mock, patch

from dto import TelegramUserDTOModel, NewSentenceDTOModel, WordDTOModel
from settings import settings
from services import CheckWordsService


class TestCheckWordsService:
    """Tests for CheckWordsService."""

    def setup_method(self):
        self._state = Mock()
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
