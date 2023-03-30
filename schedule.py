from apscheduler.schedulers.blocking import BlockingScheduler

from db.utils import add_new_text_to_db

scheduler = BlockingScheduler()
scheduler.add_job(add_new_text_to_db(), 'interval', hours=8)
# scheduler.add_job(job, 'cron', day_of_week='*', hour=12)
scheduler.start()
