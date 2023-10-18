from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import bot


class UpdateProfileService:
    """Update profile user."""

    _start_message_text: str

    def __init__(self, chat_id: int, start_message_text: str = ''):
        """Init."""
        self._chat_id = chat_id
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
        keyboard.add(InlineKeyboardButton(text='Change name', callback_data='user_profile_change_name'))
        keyboard.add(InlineKeyboardButton(text='Close', callback_data='user_profile_close'))

        await bot.send_message(chat_id=self._chat_id, text=message_text, reply_markup=keyboard)
