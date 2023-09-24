from http import HTTPStatus

from aiogram import types
from requests import get, post

from bot import dispatcher
from settings import settings


@dispatcher.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    """Handle start command."""
    print(message)
    telegram_id = message.from_user.id
    url_get_user = f'{settings.api_url}/v1/telegram_user/{telegram_id}'
    response = get(url=url_get_user, headers=settings.api_headers)

    if response.status_code == HTTPStatus.NOT_FOUND:
        url_create_user = f'{settings.api_url}/v1/telegram_user/'
        data_for_create_user = {
            'telegram_id': telegram_id,
            'level_en_id': 1,
            'main_language_id': 1,
            'experience': 0,
            'hero_level_id': 1,
            'previous_stage': '',
            'stage': 'UPDATE_PROFILE',
        }
        # response = post(url=url_create_user, headers=settings.api_headers, json=data_for_create_user)
        # print(response.json())
        text_greeting_answer = (
            '👊 Добро пожаловать в Английский Клуб!\n\n'
            'Перед тем как начать, ты должен знать основные правила:\n\n'
            '1️⃣ Первое правило Английского Клуба: рассказывайте всем об Английском Клубе. '
            'Отправьте [Ваша Ссылка] друзьям, чтобы они тоже могли присоединиться.\n'
            '2️⃣ Второе правило: НИКОГДА не забывайте о первом правиле. Кстати вот ссылка '
            '[Ваша Ссылка], чтобы рассказать всем.\n'
            '3️⃣ Третье правило: Если ты тут, то должен выполнить задание на день.'
        )
        await message.answer(text_greeting_answer)

    await message.answer("Привет! Это ваш бот.")
