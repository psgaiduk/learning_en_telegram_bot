from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from settings import settings

DATABASE_URL = settings.postgres.database_url

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db() -> Generator:
    """
    Create a database session.

    :return: A generator that yields a session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
