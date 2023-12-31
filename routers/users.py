from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import UserCreate, UserShow
from models import User
from hashing import Hasher
from database import get_db


# mini fastapi is a replica of fastapi as main
router = APIRouter()


# response model help us so user won't see all the models like password, it will see only a usershow schemas filds
@router.post("/users", tags=["user"], response_model=UserShow)
def create_user(
    user: UserCreate, db: Session = Depends(get_db)
):  # accept data from the user using the schema. user pass data
    # icreate an object
    # password I use hasher class with the func get_hash and I pass user.password to it
    user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=Hasher.get_hash_password(user.password),
    )
    # insert object into database table
    # I use db session object for it
    db.add(user)
    # I commit it save it and refresh it
    db.commit()
    db.refresh(user)
    return user
