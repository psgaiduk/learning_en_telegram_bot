from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bot import bot


class UpdateProfileService:
    """Update profile user."""

    _start_message_text: str

    def __init__(self, callback_query: CallbackQuery, state: FSMContext, start_message_text: str = ''):
        """Init."""
        self._callback_query = callback_query
        self._state = state
        self._start_message_text = start_message_text

    async def do(self) -> None:
        """Update profile user."""
        message_text = (
            f'{self._start_message_text}'
            f'Вы можете изменить своё имя или уровень английского языка.\n'
            f'Чтобы выйти из изменения профиля кликните по кнопке close.'
        )
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text='Change english level', callback_data='user_profile_change_en_level'))
        keyboard.add(InlineKeyboardButton(text='Change name', callback_data='user_pofile_change_name'))
        keyboard.add(InlineKeyboardButton(text='Close', callback_data='user_profile_close'))

        await bot.send_message(chat_id=self._callback_query.from_user.id, text=message_text, reply_markup=keyboard)
