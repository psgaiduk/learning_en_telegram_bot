from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings


engine = create_engine(f'sqlite:///{settings.path_to_database}', echo=True)
Session = sessionmaker(autoflush=False, bind=engine)
