from telegram_messenger_app.services import SendReminders


def send_reminders():
    """Send reminders for user."""
    SendReminders().work()
