# this library will create some form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from hashing import Hasher
from jose import jwt
from config import setting

# create object from this OAuth
# I have to pass url route
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")

router = APIRouter()


@router.post("/login/token", tags=["login"])
# the funct will take input form_data
def get_token_after_authentication(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # I have to veryfie if the user exists
    # I have to query user table in models.py
    # User.email==form_data.username my email is username
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username"
        )

    # verify the password
    if not Hasher.verify_password(
        form_data.password, user.password
    ):  #  user.password from database
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    data_token = {"sub": form_data.username}
    # not create token by using this data_token encode
    # pass configuration stuff like security_key and algotithm
    jwt_token = jwt.encode(data_token, setting.SECRET_KEY, setting.ALGORITHM)
    return {"access_token": jwt_token, "token_type": "bearer"}
