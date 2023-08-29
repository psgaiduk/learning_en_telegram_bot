from contextlib import contextmanager

from database import get_db


@contextmanager
def db_session():
    db_gen = get_db()
    db = next(db_gen)
    try:
        yield db
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass
