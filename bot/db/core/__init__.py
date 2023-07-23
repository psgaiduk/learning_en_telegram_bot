from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings


class DatabaseSessionManager:
    def __init__(self, commit=True, database_url=None):
        self.commit = commit
        if database_url is None:
            database_url = 'postgresql://{user}:{password}@{host}/{db_name}'.format(
                user=settings.postgres.user,
                password=settings.postgres.password,
                host=settings.postgres.host,
                db_name=settings.postgres.db_name,
            )
        echo = False
        if settings.environment == 'local':
            echo = True
        self.engine = create_engine(database_url, echo=echo)
        self.Session = sessionmaker(bind=self.engine, autoflush=True)

    def __enter__(self):
        self.session = self.Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.commit:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        self.session.close()
