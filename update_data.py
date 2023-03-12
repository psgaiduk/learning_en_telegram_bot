from db.core import engine
from db.models.base import Base


Base.metadata.create_all(bind=engine)
