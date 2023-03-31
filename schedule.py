from apscheduler.schedulers.background import BackgroundScheduler

from db.utils import add_new_text_to_db
from telegram_messenger_app.functions import send_reminders

scheduler = BackgroundScheduler()
scheduler.add_job(add_new_text_to_db(), 'interval', hours=8)
scheduler.add_job(send_reminders(), 'cron', day_of_week='*', hour=19)
scheduler.start()
