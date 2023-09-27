from aiogram import types
from requests import post

from bot import dispatcher
from functions import decode_telegram_id, encode_telegram_id
from settings import settings


@dispatcher.message_handler(state='REGISTRATION', commands=['start'])
async def handle_registration(message: types.Message):
    """Handle registration."""
    telegram_id = message.from_user.id

    url_create_user = f'{settings.api_url}/v1/telegram_user/'
    data_for_create_user = {
        'telegram_id': telegram_id,
        'level_en_id': 1,
        'main_language_id': 1,
        'experience': 0,
        'hero_level_id': 1,
        'previous_stage': '',
        'stage': 'WAIT_NAME',
    }
    post(url=url_create_user, headers=settings.api_headers, json=data_for_create_user)
    telegram_id_encode = await encode_telegram_id(telegram_id)
    telegram_link = f'https://t.me/{settings.bot_name}?start={telegram_id_encode}'
    text_greeting_answer = (
        '👊 Добро пожаловать в Английский Клуб!\n\n'
        'Перед тем как начать, ты должен знать основные правила:\n\n'
        '1️⃣ Первое правило Английского Клуба: рассказывайте всем об Английском Клубе. '
        f'Отправьте {telegram_link} друзьям, чтобы они тоже могли присоединиться.\n'
        '2️⃣ Второе правило: НИКОГДА не забывайте о первом правиле. Кстати вот ссылка '
        f'{telegram_link}, чтобы рассказать всем.\n'
        '3️⃣ Третье правило: Если ты тут, то должен выполнить задание на день.'
    )
    await message.answer(text_greeting_answer)

    text_first_day_tasks_answer = (
        '📝 Задание на первый день:\n\n'
        '1️⃣ Заполни свой профиль. Для этого нажми на кнопку "Профиль" внизу экрана.\n'
        '2️⃣ Прочитать 5 предложений.\n'
    )

    await message.answer(text_first_day_tasks_answer)

    if '/start' in message.text:
        friend_telegram_id = message.text.split('/start ')[1]
        if not friend_telegram_id:
            return None
        decode_friend_telegram_id = await decode_telegram_id(friend_telegram_id)
        url_create_referral = f'{settings.api_url}/v1/referrals/'
        data_for_create_referral = {
            'telegram_user_id': decode_friend_telegram_id,
            'friend_telegram_id': telegram_id,
        }
        post(url=url_create_referral, headers=settings.api_headers, json=data_for_create_referral)
