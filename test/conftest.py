# keep this conftest.py always like that because when you run the pytest fisr pytest reads this conf file

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
from database import Base, get_db
from config import setting
from models import User


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a medadata to sqlite table
Base.metadata.create_all(bind=engine)


# it is a fixture
# this will run before executing test cases
@pytest.fixture
def client():
    # override get_db function
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
            app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    yield client


@pytest.fixture
def header_token(client: TestClient):
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == setting.TEST_EMAIL).first()
    if user is None:
        user_add_db = User(email=setting.TEST_EMAIL, password=setting.TEST_PASSWORD)
        user_add = db.add(user_add_db)
        db.commit()
        db.add(user_add)
    data = {"username": setting.TEST_EMAIL, "password": setting.TEST_PASSWORD}
    response = client.post(
        "/login/token", data=data
    )  # this route will be triger when posting this username, password
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
