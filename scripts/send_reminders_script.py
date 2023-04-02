from loguru import logger

from telegram_messenger_app.functions import send_reminders
import os
import sys

project_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root_path)

if __name__ == "__main__":
    logger.configure(extra={'chat_id': 1, 'work_id': 1})
    send_reminders()
