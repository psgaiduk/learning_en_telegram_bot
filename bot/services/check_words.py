from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.storage import FSMContext

from bot import bot
from choices import State
from dto import TelegramUserDTOModel, WordDTOModel
from functions import update_data_by_api


class CheckWordsService:
    """Check words before sentence."""

    _state: FSMContext
    _start_text_message: str
    _telegram_user: TelegramUserDTOModel
    _words: list
    _first_word: WordDTOModel

    def __init__(self, state: FSMContext, start_text_message: str = '') -> None:
        """Init."""
        self._state = state
        self._start_text_message = start_text_message

    async def do(self) -> None:
        """Check words before sentence."""
        await self._get_user()
        self._words = self._telegram_user.new_sentence.words
        self._first_word = self._words.pop(0)

        if await self._update_user() is False:
            return

        if await self._update_sentence() is False:
            return

        await self._state.set_data(data={'user': self._telegram_user})

        await self._send_message()

    async def _get_user(self) -> None:
        data = await self._state.get_data()
        self._telegram_user = data['user']

    async def _update_user(self) -> bool:
        data_for_update_user = {
            'telegram_id': self._telegram_user.telegram_id,
            'stage': State.read_book.value,
        }

        return await update_data_by_api(
            telegram_id=self._telegram_user.telegram_id,
            params_for_update=data_for_update_user,
            url_for_update=f'telegram_user/{self._telegram_user.telegram_id}',
        )

    async def _update_sentence(self) -> bool:
        words_ids = [word.word_id for word in self._words]

        data_for_update_history_sentence = {
            'id': self._telegram_user.new_sentence.history_sentence_id,
            'check_words': words_ids,
        }

        return await update_data_by_api(
            telegram_id=self._telegram_user.telegram_id,
            params_for_update=data_for_update_history_sentence,
            url_for_update=f'history/sentences/{self._telegram_user.new_sentence.history_sentence_id}',
        )


    async def _send_message(self) -> None:
        inline_keyboard = InlineKeyboardMarkup()
        inline_keyboard.add(InlineKeyboardButton(text='I know', callback_data=f'know_word_true_{self._first_word.word_id}'))
        inline_keyboard.add(InlineKeyboardButton(text='I don\'t know', callback_data=f'know_word_false_{self._first_word.word_id}'))

        text_message = f'{self._start_text_message}Слово: {self._first_word.word}\nПеревод: {self._first_word.translation["ru"]}'
        await bot.send_message(chat_id=self._telegram_user.telegram_id, text=text_message, reply_markup=inline_keyboard)
