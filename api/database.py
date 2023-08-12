from sqlalchemy import MetaData
from databases import Database
from sqlalchemy.ext.declarative import declarative_base
import settings

DATABASE_URL = settings.DATABASE_URL

database = Database(DATABASE_URL)
metadata = MetaData()

Base = declarative_base(metadata=metadata)
