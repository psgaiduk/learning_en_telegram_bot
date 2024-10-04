from pytest import fixture

from database import engine, Base


@fixture(scope="function", autouse=True)
def create_test_database():
    """Delete and Create test database."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
