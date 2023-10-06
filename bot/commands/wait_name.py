from http import HTTPStatus
from re import match

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot import dispatcher
from context_managers import http_client
from settings import settings


@dispatcher.message_handler(lambda message: message.text and match(r'^[\w]+$', message.text), state='WAIT_NAME')
async def handle_wait_name(message: Message, state: FSMContext):
    """Handle wait name."""
    data = await state.get_data()
    telegram_user = data['user']
    telegram_id = telegram_user['telegram_id']
    new_name = message.text.title()

    inline_kb = InlineKeyboardMarkup()

    if telegram_user['previous_stage'] == 'NEW_CLIENT':
        stage = 'WAIT_EN_LEVEL'
        message_text = (f'Имя профиля изменено на {new_name}.\n'
                        f'Выберите уровень знаний английского языка. Сейчас вам доступны 2 первых уровня, '
                        f'но с увлечинием уровня, будут открываться новые уровни знаний.')
        inline_kb.add(InlineKeyboardButton(text='A1 - Beginner', callback_data='level_en_1'))
        inline_kb.add(InlineKeyboardButton(text='A2 - Elementary', callback_data='level_en_2'))
        if telegram_user['hero_level']['order'] > 10:
            inline_kb.add(InlineKeyboardButton(text='B1 - Pre-intermediate', callback_data='level_en_3'))
        if telegram_user['hero_level']['order'] > 25:
            inline_kb.add(InlineKeyboardButton(text='B2 - Intermediate', callback_data='level_en_4'))
        if telegram_user['hero_level']['order'] > 50:
            inline_kb.add(InlineKeyboardButton(text='C1 - Upper-intermediate', callback_data='level_en_5'))
        if telegram_user['hero_level']['order'] > 80:
            inline_kb.add(InlineKeyboardButton(text='C2 - Advanced', callback_data='level_en_6'))

    else:
        stage = 'UPDATE_PROFILE'
        inline_kb.add(InlineKeyboardButton(text='Change english level', callback_data='user_profile_change_en_level'))
        inline_kb.add(InlineKeyboardButton(text='Change name', callback_data='user_pofile_change_name'))
        inline_kb.add(InlineKeyboardButton(text='Close', callback_data='user_profile_close'))
        message_text = f'Имя профиля изменено на {new_name}.\nВыберите дальнейшее действие:'

    async with http_client() as client:
        url_update_telegram_user = f'{settings.api_url}/v1/telegram_user/{telegram_id}'
        data_for_update_user = {
            'telegram_id': telegram_id,
            'user_name': new_name,
            'stage': stage,
        }
        _, response_status = await client.patch(
            url=url_update_telegram_user,
            headers=settings.api_headers,
            json=data_for_update_user,
        )

    if response_status == HTTPStatus.OK:
        await message.answer(text=message_text, reply_markup=inline_kb)
    else:
        await message.answer(text='🤖 Что-то пошло не так. Попробуйте еще раз, чуть позже.')


@dispatcher.message_handler(lambda message: message.text and not match(r'^[\w]+$', message.text), state='WAIT_NAME')
async def handle_wait_name_incorrect_work(message: Message):
    """Handle wait name."""
    await message.answer('Имя надо вводить одним слово, без использования специальных символов. Попробуйте еще раз.')