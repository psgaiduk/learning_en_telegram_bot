from typing import List
from random import choice

from db.choices import RemindersType
from bot.bot import get_text_reminders
from bot.bot import get_users_who_not_read_today
from db.models import TextReminder, Users
from telegram_messenger_app.core import TelegramSDK


class SendReminders:
    """Send message than need to read texts."""

    _reminders_by_direction: dict
    _start_reminders: List[TextReminder]
    _end_reminders: List[TextReminder]
    _users_for_reminder: List[Users]

    def __init__(self) -> None:
        """Init."""
        self._telegram_sdk = TelegramSDK()
        self._reminders_by_direction = {}

    def work(self) -> None:
        """Send messages."""
        self._get_reminders()
        self._users_for_reminder = get_users_who_not_read_today()

        if self._users_for_reminder:
            self._send_message()

    def _get_reminders(self) -> None:
        reminders = get_text_reminders()
        self._start_reminders = [reminder for reminder in reminders
                                 if reminder.type_reminder == RemindersType.start_read_text.value]
        self._end_reminders = [reminder for reminder in reminders
                               if reminder.type_reminder == RemindersType.end_read_text.value]

    def _send_message(self):
        for user in self._users_for_reminder:
            start_reminder = self._get_reminder(
                type_reminder=choice(self._start_reminders),
                language=user.learn_language)
            end_reminder = self._get_reminder(
                type_reminder=choice(self._end_reminders),
                language=user.main_language)

            reminder_text = f'{start_reminder} {end_reminder}'
            self._telegram_sdk.send_message(
                telegram_id=user.telegram_id,
                message=reminder_text,
            )

    def _get_reminder(self, type_reminder: TextReminder, language: str) -> str:
        language_reminder = {
            'ru': type_reminder.ru,
            'en': type_reminder.en,
            'fr': type_reminder.fr,
            'es': type_reminder.es,
            'ge': type_reminder.ge,
        }

        return language_reminder.get(language)


if __name__ == '__main__':
    SendReminders().work()
