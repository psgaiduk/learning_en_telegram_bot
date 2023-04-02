from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger

from db.utils import add_new_text_to_db
from telegram_messenger_app.functions import send_reminders

scheduler = BlockingScheduler()


def start_scheduler():
    logger.configure(extra={'chat_id': 1, 'work_id': datetime.now().timestamp()})
    logger.info('start schedule')
    scheduler.add_job(add_new_text_to_db, 'interval', hours=8)
    scheduler.add_job(send_reminders, 'cron', day_of_week='*', hour=19)
    scheduler.start()
