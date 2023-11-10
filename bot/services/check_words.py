from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.storage import FSMContext

from bot import bot
from choices import State
from functions import update_data_by_api


class CheckWordsService:
    """Check words before sentence."""

    def __init__(self, state: FSMContext, start_text_message: str = '') -> None:
        """Init."""
        self._state = state
        self._start_text_message = start_text_message

    async def do(self):
        """Check words before sentence."""

        await self._get_user()
        self._words = self._telegram_user.new_sentence.words
        first_word = self._words.pop(0)

        if await self._update_user() is False:
            return

        if await self._update_sentence() is False:
            return

        inline_keyboard = InlineKeyboardMarkup()
        inline_keyboard.add(InlineKeyboardButton(text='Знаю', callback_data=f'know_word_true_{first_word.word_id}'))
        inline_keyboard.add(InlineKeyboardButton(text='Не знаю', callback_data=f'know_word_false_{first_word.word_id}'))

        text_message = f'{self._start_text_message}Слово: {first_word.word}\nПеревод: {first_word.translation["ru"]}'
        await bot.send_message(chat_id=self._telegram_user.telegram_id, text=text_message, reply_markup=inline_keyboard)
        
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

    async def _update_sentence(self):
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