from fastapi import APIRouter, Request, Depends, Response
from fastapi.templating import Jinja2Templates
from models import User
from sqlalchemy.orm import Session
from database import get_db
from hashing import Hasher
from config import setting
from jose import jwt

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")


@router.get("/login")
def login(request: Request, msg: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "msg": msg})


@router.post("/login")
async def login(response: Response, request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    errors = []
    if not email:
        errors.append("Please enter valid email")
    if not password:
        errors.append("Enter password")
    if len(errors) > 0:
        return templates.TemplateResponse(
            "login.html", {"request": request, "errors": errors}
        )
    try:
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            errors.append("Emial does not exist. Create an account")
            return templates.TemplateResponse(
                "login.html", {"request": request, "errors": errors}
            )
        else:
            # check if password are == this one from db and what users add
            if Hasher.verify_password(password, user.password):
                # create jwt token
                data = {"sub": email}
                jwt_token = jwt.encode(
                    data, setting.SECRET_KEY, algorithm=setting.ALGORITHM
                )
                msg = "Login successful"
                response = templates.TemplateResponse(
                    "login.html", {"request": request, "msg": msg}
                )
                response.set_cookie(
                    key="access_token", value=f"Bearer {jwt_token}", httponly=True
                )
                return response
            else:
                errors.append("Invalid Password")
                return templates.TemplateResponse(
                    "login.html", {"request": request, "errors": errors}
                )
    except:
        errors.append("Something went wrong")
        return templates.TemplateResponse(
            "login.html", {"request": request, "errors": errors}
        )
