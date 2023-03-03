from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base
from settings import settings


engine = create_engine(f'sqlite:///{settings.path_to_database}', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(autoflush=False, bind=engine)
