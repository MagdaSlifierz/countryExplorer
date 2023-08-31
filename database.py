from config import setting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator

SQLALCHEMY_DATABASE_URL = setting.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

#session local and for this session we create get_db function
SessionLocal = sessionmaker(autcommit=False, autoflush=False, bind=engine)


Base = declarative_base()

# function for dependency injection. Finally block always will be execute. It will close database
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()