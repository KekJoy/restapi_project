from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config_data import config

engine = create_engine(config.DB_PATH)
conn = engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Получение сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
