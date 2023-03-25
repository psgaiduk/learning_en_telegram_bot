from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from db.functions.users import update_user_level
from telegram_bot_app.core import dispatcher
from telegram_bot_app.functions import get_user_by_chat_id
from telegram_bot_app.states import SettingsStates


@dispatcher.callback_query_handler(state=SettingsStates.start_settings)
async def update_settings(query: types.CallbackQuery, state: FSMContext):
    """Update settings."""

    callback_data = query.data
    logger.debug(f'get callback data = {callback_data}')

    chat_id = query.from_user.id
    user = await get_user_by_chat_id(chat_id=chat_id, name=query.from_user.first_name)

    if 'level' in callback_data:
        level = int(callback_data.split('_')[1])
        await update_user_level(telegram_id=chat_id, level=level)

        answer_text = f'{user.name}, вот твои настройки обновлены:\nНовый уровень сложности: {level}'
        await query.answer(answer_text)
        await query.message.delete()

        await state.finish()
