from copy import deepcopy

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytest import mark, fixture
from unittest.mock import ANY, AsyncMock, patch

from bot import bot
from choices import State
from services import CheckWordsService
from tests.fixtures import *  # noqa: F401, F403


class TestCheckWordsService:
    """Tests for CheckWordsService."""

    @fixture(autouse=True)
    def setup_method(self, telegram_user_with_sentence_and_word):
        self._state = AsyncMock()
        self._telegram_user = telegram_user_with_sentence_and_word
        self._chat_id = self._telegram_user.telegram_id

    @mark.asyncio
    async def test_do_all_true(self):
        service = CheckWordsService(state=self._state, start_text_message="")

        mock_get_user = AsyncMock(return_value=None)
        service._get_user = mock_get_user
        service._telegram_user = deepcopy(self._telegram_user)

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
        assert service._first_word == self._telegram_user.new_sentence.words[0]

    @mark.asyncio
    async def test_do_update_user_false(self):
        service = CheckWordsService(state=self._state, start_text_message="")

        mock_get_user = AsyncMock(return_value=None)
        service._get_user = mock_get_user
        service._telegram_user = deepcopy(self._telegram_user)

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
        service = CheckWordsService(state=self._state, start_text_message="")

        mock_get_user = AsyncMock(return_value=None)
        service._get_user = mock_get_user
        service._telegram_user = deepcopy(self._telegram_user)

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
        service = CheckWordsService(state=self._state, start_text_message="")

        self._state.get_data = AsyncMock(return_value={"user": self._telegram_user})

        await service._get_user()

        assert service._telegram_user == self._telegram_user

    @mark.parametrize("update_status", [True, False])
    @mark.asyncio
    @patch("services.check_words.update_data_by_api", new_callable=AsyncMock)
    async def test_update_user(self, mock_update_user, update_status):
        service = CheckWordsService(state=self._state, start_text_message="")
        service._telegram_user = deepcopy(self._telegram_user)

        mock_update_user.side_effect = [update_status]

        return_value = await service._update_user()

        mock_update_user.assert_called_once_with(
            telegram_id=self._telegram_user.telegram_id,
            params_for_update={
                "telegram_id": self._telegram_user.telegram_id,
                "stage": State.read_book.value,
            },
            url_for_update=f"telegram_user/{self._telegram_user.telegram_id}",
        )

        assert return_value is update_status

    @mark.parametrize("update_status", [True, False])
    @mark.asyncio
    @patch("services.check_words.update_data_by_api", new_callable=AsyncMock)
    async def test_update_sentence(self, mock_update_user, update_status):
        service = CheckWordsService(state=self._state, start_text_message="")
        service._telegram_user = deepcopy(self._telegram_user)
        service._words = deepcopy(self._telegram_user.new_sentence.words)

        mock_update_user.side_effect = [update_status]

        return_value = await service._update_sentence()

        words_ids = [word.word_id for word in self._telegram_user.new_sentence.words]

        mock_update_user.assert_called_once_with(
            telegram_id=self._telegram_user.telegram_id,
            params_for_update={
                "id": self._telegram_user.new_sentence.history_sentence_id,
                "check_words": words_ids,
            },
            url_for_update=f"history/sentences/{self._telegram_user.new_sentence.history_sentence_id}",
        )

        assert return_value is update_status

    @mark.parametrize("start_message_text", ["", "Text", "Another text"])
    @mark.asyncio
    async def test_send_message(self, start_message_text):
        service = CheckWordsService(state=self._state, start_text_message="")
        service._telegram_user = deepcopy(self._telegram_user)
        word = deepcopy(self._telegram_user.new_sentence.words)[0]
        service._first_word = word
        service._start_text_message = start_message_text

        with patch.object(bot, "send_message", new=AsyncMock()) as mock_send_message:
            await service._send_message()

            excepted_text = (
                f'{start_message_text}\nТы знаешь это слово?\n\n'
                f'Слово: {word.word} - {word.transcription}\nПеревод: {word.translation["ru"]}'
            )

            mock_send_message.assert_called_once_with(
                chat_id=self._chat_id,
                text=excepted_text,
                reply_markup=ANY,
            )

            reply_markup_call = mock_send_message.call_args_list[0]
            reply_markup = reply_markup_call.kwargs["reply_markup"]

            assert isinstance(reply_markup, InlineKeyboardMarkup)
            assert reply_markup.inline_keyboard == [
                [InlineKeyboardButton(text="Знаю", callback_data=f"know_word_true_{word.word_id}")],
                [InlineKeyboardButton(text="Не знаю", callback_data=f"know_word_false_{word.word_id}")],
            ]
