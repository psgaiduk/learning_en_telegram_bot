from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings


engine = create_engine(f'postgresql://{settings.postgres.user}:{settings.postgres.password}@{settings.postgres.host}/{settings.postgres.db_name}', echo=True)
Session = sessionmaker(autoflush=False, bind=engine)
