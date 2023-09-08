from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
from database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#create a medadata to sqlite table
Base.metadata.create_all(bind=engine)

#override get_db function
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)

#defind test case
def test_create_user():
    data = {
        "first_name" : "Jolanta",
        "last_name" : "Kwasniewska", 
        "email" : "j.k@gmail.com", 
        "password" : "Jolanta123"
        }
    response = client.post("/users", json=data) #json.dumps(data)) this change our data to json reprensetation
    assert response.status_code == 200
    assert response.json()["first_name"] == "Jolanta"
    assert response.json()["last_name"] == "Kwasniewska"
    assert response.json()["email"] == "j.k@gmail.com"
    assert response.json()["is_active"] is True