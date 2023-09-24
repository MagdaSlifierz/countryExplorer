from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# get for form 
@router.get("/register")
def registration(request: Request):
    return templates.TemplateResponse("user_register.html", {"request": request})

# submit the form post operation
@router.post("/register")
def registration(request: Request, db: Session=Depends(get_db)):
    # I have to read the form accept the form
    form = request.form() # it will accept the fields from the forms
    print(form)