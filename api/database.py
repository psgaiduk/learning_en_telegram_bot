from sqlalchemy import MetaData
from databases import Database
from sqlalchemy.ext.declarative import declarative_base
from settings import settings

DATABASE_URL = settings.postgres.database_url

database = Database(DATABASE_URL)
metadata = MetaData()

Base = declarative_base(metadata=metadata)
