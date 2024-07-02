from aiogram.types import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from loguru import logger

from bot import bot
from dto import TelegramUserDTOModel, WordDTOModel
from functions import send_message_learn_word, update_learn_word


class LearnWordsService:
    """Service for learn words after sentence."""

    telegram_user: TelegramUserDTOModel
    state: FSMContext
    message: CallbackQuery
    first_word: WordDTOModel = None

    def __init__(self, message: CallbackQuery, state: FSMContext) -> None:
        """Init."""
        self.message = message
        self.state = state

    async def do(self) -> None:
        """Start work service."""

        await self._get_user()
        await self._get_first_word()
        is_update = await update_learn_word(message=self.message, word=self.first_word)
        if not is_update:
            return await bot.send_message(
                chat_id=self.message.from_user.id,
                text='Что-то пошло не так, попробуй ещё раз',
            )

        await self.state.set_data(data={'user': self.telegram_user})  # Обновляем состояние без первого слова в learn_words
        if self.telegram_user.learn_words:
            await send_message_learn_word(word=self.telegram_user.learn_words[0], telegram_id=self.telegram_user.telegram_id, message=self.message)

    async def _get_user(self) -> None:
        data = await self.state.get_data()
        self.telegram_user = data['user']

    async def _get_first_word(self) -> None:
        self.first_word = self.telegram_user.learn_words.pop(0)
        logger.debug(f'first word = {self.first_word},{self.message}')
