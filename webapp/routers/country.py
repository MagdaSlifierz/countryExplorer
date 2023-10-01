from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from models import Country
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")

@router.get("/")
def home(request: Request, db: Session=Depends(get_db), msg:str=None):
    countries = db.query(Country).all()
    return templates.TemplateResponse("home.html", {"request" : request, "countries": countries, "msg":msg})


@router.get("/detail/{country_id}")
def country_detail(request: Request, country_id: int, db: Session=Depends(get_db)):
    country = db.query(Country).filter(Country.country_id==country_id).first()
    return templates.TemplateResponse("country_detail.html", {"request" : request, "country" : country})

@router.post("/create-country")
def create_country(reqest: Request, db: Session=Depends(get_db)):
    return templates.TemplateResponse("create_country.html", {"reqest" : reqest})

