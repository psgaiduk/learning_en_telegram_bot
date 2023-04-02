from loguru import logger
from telegram_messenger_app.services import SendReminders


def send_reminders():
    """Send reminders for user."""
    logger.info('start reminder')
    SendReminders().work()
