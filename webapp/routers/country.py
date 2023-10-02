from fastapi import APIRouter, Request, Depends, status, responses
from fastapi.templating import Jinja2Templates
from models import Country, User
from sqlalchemy.orm import Session
from database import get_db
from jose import jwt
from config import setting


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

@router.get("/create-country")
def create_country(request: Request):
    return templates.TemplateResponse("create_country.html", {"request" : request})

@router.post("/create-country")
async def create_country(request: Request, db: Session=Depends(get_db)):
    #take the form
    form = await request.form()
    country_name  = form.get("country_name")
    capital = form.get("capital")
    official_lang = form.get("official_lang")
    area = form.get("area")
    description = form.get("description")
    
    errors = []
    if not country_name:
        errors.append("You have to enter the name of a new country that you want to learn about it ")
    
    if not description:
        errors.append("Description should be added ")

    if len(errors) > 0:
        return templates.TemplateResponse("create_country.html", {"request" : request, "errors": errors})
    
    # retrive the token from the cookie. 
    # the form title and browser data are send

    try:
        token = request.cookies.get("access_token")
        if not token:
            errors.append("Create account or Login")
            return templates.TemplateResponse("create_country.html", {"request" : request, "errors": errors})
        
        scheme, _, param = token.partition(" ")
            #now decoded the token because i need the payload 
            # takes the email from the people who is owner of the post
        payload = jwt.decode(param, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
        email = payload.get("sub")
            # take ID from database that is associate with this email
        if email is None:
            errors.append("This user doesn't exist. Create account")
            return templates.TemplateResponse("create_country.html", {"request" : request, "errors": errors})
        else:
            user = db.query(User).filter(User.email == email).first()
            if user is None:
                errors.append("You are not authenticated, Kindly Login")
                return templates.TemplateResponse( "create_item.html", {"request": request, "errors": errors})
            else:
                # create object of the class
                country = Country(country_name=country_name, capital=capital, official_lang=official_lang, area=area,
                                description=description, user_creator_id=user.user_id)
                db.add(country)
                db.commit()
                db.refresh(country)
                return responses.RedirectResponse(f"/detail/{country.country_id}",status_code=status.HTTP_302_FOUND)
    except Exception as e:
        errors.append("Something went wrong")
        print(e)
        return templates.TemplateResponse(
            "create_country.html", {"request": request, "errors": errors})

