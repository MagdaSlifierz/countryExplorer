from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from hashing import Hasher
from models import User
from sqlalchemy.exc import IntegrityError

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# get for form 
@router.get("/register")
def registration(request: Request):
    return templates.TemplateResponse("user_register.html", {"request": request})

# submit the form post operation
@router.post("/register")
async def registration(request: Request, db: Session=Depends(get_db)):
    # I have to read the form accept the form
    form = await request.form() # it will accept the fields from the forms
    first_name = form.get("first_name")
    last_name = form.get("last_name")
    email = form.get("email")
    password = form.get("password")
    errors = []
    if len(password) < 6:
        errors.append("Password should be greater that 6 characters")
        return templates.TemplateResponse("user_regster.html", {"request":request, "errors": errors})
    # entering to the database store into it
    user = User(first_name=first_name, last_name=last_name, email=email,  password=Hasher.get_hash_password(password))
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        # this time redirect to home page
        #pass message to query parameter
        return responses.RedirectResponse("/?msg=Successfully Registered", status_code=status.HTTP_302_FOUND)
    except IntegrityError:
        errors.append("Email already exists")
        return templates.TemplateResponse("user_register.html", {"request":request, "errors": errors})

    