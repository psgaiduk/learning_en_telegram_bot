from loguru import logger

from telegram_messenger_app.functions import send_reminders

if __name__ == "__main__":
    logger.configure(extra={'chat_id': 1, 'work_id': 1})
    send_reminders()
