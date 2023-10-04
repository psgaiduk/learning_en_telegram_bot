from http import HTTPStatus

from aiogram import types

from context_managers import http_client
from functions import decode_telegram_id, encode_telegram_id
from settings import settings


class RegistrationService:
    """Registration telegram user."""

    def __init__(self, message: types.Message):
        """Init."""
        self._message = message
        self._telegram_id = self._message.from_user.id

    async def do(self):
        """Registration."""
        await self._create_user()
        await self._send_greeting_message()
        await self._send_tasks_today()
        if '/start' in self._message.text:
            await self._create_referral()

    async def _create_user(self) -> None:
        url_create_user = f'{settings.api_url}/v1/telegram_user/'
        data_for_create_user = {
            'telegram_id': self._telegram_id,
            'main_language_id': 1,
            'experience': 0,
            'hero_level_id': 1,
            'previous_stage': '',
            'stage': 'WAIT_NAME',
        }
        async with http_client() as client:
            _, response_status = await client.post(
                url=url_create_user, headers=settings.api_headers, json=data_for_create_user)

        if response_status != HTTPStatus.CREATED:
            text_somthing_wrong_answer = '🤖 Что-то пошло не так. Попробуйте еще раз, чуть позже.'
            await self._message.answer(text_somthing_wrong_answer)

    async def _send_greeting_message(self) -> None:
        telegram_id_encode = await encode_telegram_id(self._telegram_id)
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
        await self._message.answer(text_greeting_answer)

    async def _send_tasks_today(self) -> None:
        text_first_day_tasks_answer = (
            '📝 Задание на первый день:\n\n'
            '1️⃣ Заполни свой профиль. Для этого нажми на кнопку "Профиль" внизу экрана.\n'
            '2️⃣ Прочитать 5 предложений.\n'
        )

        await self._message.answer(text_first_day_tasks_answer)

    async def _create_referral(self) -> None:
        friend_telegram_id = None
        if '/start ' in self._message.text:
            friend_telegram_id = self._message.text.split('/start ')[1]
        if not friend_telegram_id:
            return None
        decode_friend_telegram_id = await decode_telegram_id(friend_telegram_id)
        if not decode_friend_telegram_id:
            return None
        url_create_referral = f'{settings.api_url}/v1/referrals/'
        data_for_create_referral = {
            'telegram_user_id': decode_friend_telegram_id,
            'friend_telegram_id': self._telegram_id,
        }
        async with http_client() as client:
            await client.post(url=url_create_referral, headers=settings.api_headers, json=data_for_create_referral)
