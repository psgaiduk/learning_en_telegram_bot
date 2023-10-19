from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.filters import Text

from bot import bot, dispatcher
from choices import State
from functions import update_user_state
from services import UpdateProfileService


@dispatcher.message_handler(state=State.update_profile.value, commands='profile')
async def handle_update_profile(message: Message):
    """Handle update profile."""

    is_update = await update_user_state(telegram_id=message.from_user.id, state=State.update_profile.value)

    if is_update is False:
        return

    await UpdateProfileService(chat_id=message.from_user.id, start_message_text='').do()


@dispatcher.callback_query_handler(Text(equals='user_profile_change_name'), state=State.update_profile.value)
async def handle_update_profile_name(callback_query: CallbackQuery):
    """Handle update profile."""

    is_update = await update_user_state(telegram_id=callback_query.from_user.id, state=State.wait_name.value)

    if is_update is False:
        return

    message_text = 'Введите ваше имя:'
    await bot.send_message(chat_id=callback_query.from_user.id, text=message_text)
