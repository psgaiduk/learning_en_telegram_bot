import os
import sys

# Используйте абсолютный путь к корневому каталогу вашего проекта
project_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root_path)


from loguru import logger

from db.utils import add_new_text_to_db


if __name__ == "__main__":
    logger.configure(extra={'chat_id': 1, 'work_id': 1})
    add_new_text_to_db()
