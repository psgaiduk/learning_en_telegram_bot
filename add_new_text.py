from time import sleep

from db.utils import add_new_text_to_db

if __name__ == '__main__':
    eight_hours_in_seconds = 60 * 60 * 8
    while True:
        add_new_text_to_db()
        sleep(eight_hours_in_seconds)
