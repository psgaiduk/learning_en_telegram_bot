from loguru import logger

from db.utils import add_new_text_to_db

if __name__ == "__main__":
    logger.configure(extra={'chat_id': 1, 'work_id': 1})
    add_new_text_to_db()
