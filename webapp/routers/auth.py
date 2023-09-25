from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

router = APIRouter(include_in_schema=False)
template = Jinja2Templates(directory="templates")

@router.get("/login")
def login(request: Request):
    return template.TemplateResponse("login.html", {"request":request})