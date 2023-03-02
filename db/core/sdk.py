from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base, User
from settings import settings


engine = create_engine(f'sqlite:///{settings.path_to_database}', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(autoflush=False, bind=engine)

# Create
with Session() as session:
    tom = User(telegram_id=1, name='Tom')
    session.add(tom)     # добавляем в бд
    session.commit()     # сохраняем изменения
    session.refresh(tom)
    print(tom.telegram_id)   # можно получить установленный id


# Read
with Session() as session:
    # получение всех объектов
    user = session.query(User).filter(User.telegram_id == 1).first()
    print(user)


# Update
with Session() as session:
    # получаем один объект, у которого id=1
    tom = session.query(User).filter(User.telegram_id == 1).first()
    if tom:
        tom.name = "Tomas"
        session.commit()  # сохраняем изменения

# Delete
with Session() as session:
    tom = session.query(User).filter(User.telegram_id == 1).first()
    session.delete(tom)  # удаляем объект
    session.commit()     # сохраняем изменения