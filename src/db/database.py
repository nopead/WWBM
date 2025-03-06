from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import DSN


def get_session():
    engine = create_engine(url=DSN, pool_size=50, echo=False)
    session = sessionmaker(bind=engine)()
    yield session