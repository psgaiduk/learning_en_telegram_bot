from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from bot import bot, dispatcher
from choices import State
from dto.telegram_user import TelegramUserDTOModel
from functions import create_keyboard_for_en_levels, update_user
from services import UpdateProfileService


@dispatcher.message_handler(state=State.update_profile.value, commands='profile')
async def handle_update_profile(message: Message):
    """Handle update profile."""

    params_for_update_user = {
        'telegram_id': message.from_user.id,
        'stage': State.update_profile.value,
    }

    is_update = await update_user(telegram_id=message.from_user.id, params_for_update=params_for_update_user)

    if is_update is False:
        return

    await UpdateProfileService(chat_id=message.from_user.id, start_message_text='').do()


@dispatcher.callback_query_handler(Text(equals='user_profile_change_name'), state=State.update_profile.value)
async def handle_update_profile_name(callback_query: CallbackQuery):
    """Handle update profile."""

    params_for_update_user = {
        'telegram_id': callback_query.from_user.id,
        'stage': State.wait_name.value,
    }

    is_update = await update_user(telegram_id=callback_query.from_user.id, params_for_update=params_for_update_user)

    if is_update is False:
        return

    message_text = 'Введите ваше имя:'
    await bot.send_message(chat_id=callback_query.from_user.id, text=message_text)


@dispatcher.callback_query_handler(Text(equals='user_profile_change_en_level'), state=State.update_profile.value)
async def handle_update_profile_en_level(callback_query: CallbackQuery, state: FSMContext):
    """Handle update profile."""

    params_for_update_user = {
        'telegram_id': callback_query.from_user.id,
        'stage': State.wait_en_level.value,
    }

    is_update = await update_user(telegram_id=callback_query.from_user.id, params_for_update=params_for_update_user)

    if is_update is False:
        return

    data = await state.get_data()
    telegram_user: TelegramUserDTOModel = data['user']

    inline_kb = await create_keyboard_for_en_levels(hero_level=telegram_user.hero_level.order)

    message_text = 'Выберите уровень сложности: '
    await bot.send_message(chat_id=callback_query.from_user.id, text=message_text, reply_markup=inline_kb)


@dispatcher.callback_query_handler(Text(equals='user_profile_close'), state=State.update_profile.value)
async def handle_update_profile_close(callback_query: CallbackQuery, state: FSMContext):
    """Handle update profile close."""

    data = await state.get_data()
    telegram_user: TelegramUserDTOModel = data['user']

    params_for_update_user = {
        'telegram_id': callback_query.from_user.id,
        'stage': telegram_user.previous_stage,
        'previous_stage': '',
    }

    is_update = await update_user(telegram_id=callback_query.from_user.id, params_for_update=params_for_update_user)

    if is_update is False:
        return

    message_text = 'Настройка профиля завершена.'
    await bot.send_message(chat_id=callback_query.from_user.id, text=message_text)


@dispatcher.callback_query_handler(state=State.update_profile.value)
@dispatcher.message_handler(state=State.update_profile.value)
async def handle_update_profile_other_data(callback_query: CallbackQuery):
    """Handle update profile for other data."""

    message_text = 'Нужно кликнуть по кнопке, чтобы продолжить настройку профиля.'
    await bot.send_message(chat_id=callback_query.from_user.id, text=message_text)
