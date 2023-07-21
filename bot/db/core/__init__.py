from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bot.settings import settings


engine = create_engine(
    'postgresql://{user}:{password}@{host}/{db_name}'.format(
        user=settings.postgres.user,
        password=settings.postgres.password,
        host=settings.postgres.host,
        db_name=settings.postgres.db_name,
    ),
    echo=True,
)
Session = sessionmaker(autoflush=False, bind=engine)
