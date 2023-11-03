from fastapi import APIRouter, Request, Depends, status, responses, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from models import Country, User
from sqlalchemy.orm import Session
from database import get_db
from jose import jwt
from config import setting
from typing import Optional
from fastapi.responses import HTMLResponse
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image
from routers.login import oauth2_scheme


router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")


@router.get("/")
def home(request: Request, db: Session = Depends(get_db), msg: str = None):
    countries = db.query(Country).all()
    return templates.TemplateResponse(
        "home.html", {"request": request, "countries": countries, "msg": msg}
    )

@router.get("/home/", response_class=HTMLResponse)
async def get_items(request: Request, page: int = 1, page_size: int = 5):
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_items = Country[start_idx:end_idx]
    total_items = len(Country)
    total_pages = (total_items + page_size - 1) // page_size
    prev_page = page - 1 if page > 1 else 1
    next_page = page + 1 if page < total_pages else total_pages

    return templates.TemplateResponse(
        "home.html",
        {"request": request, "items": paginated_items, "page": page, "total_pages": total_pages, "prev_page": prev_page, "next_page": next_page},
    )


@router.get("/detail/{country_id}")
def country_detail(request: Request, country_id: int, db: Session = Depends(get_db)):
    country = db.query(Country).filter(Country.country_id == country_id).first()
    email = db.query(User).filter(User.user_id == country.user_creator_id).first()
    country.country_image = f"static/images/{country.country_image}"
    return templates.TemplateResponse(
        "country_detail.html", {"request": request, "country": country, "email" : email})


@router.get("/update/{country_id}")
def update_country(request: Request, country_id: int, db: Session=Depends(get_db)):
    country = db.query(Country).filter(Country.country_id == country_id).first()
    return templates.TemplateResponse(
        "update_country.html", {"request": request, "country": country}
    )


@router.get("/create-country")
def create_country(request: Request):
    return templates.TemplateResponse("create_country.html", {"request": request})


@router.post("/create-country")
async def create_country(request: Request, db: Session = Depends(get_db)):
    # take the form
    form = await request.form()
    country_name = form.get("country_name")
    capital = form.get("capital")
    official_lang = form.get("official_lang")
    area = form.get("area")
    description = form.get("description")

    errors = []
    if not country_name:
        errors.append(
            "You have to enter the name of a new country that you want to learn about it "
        )
    
    if not description:
        errors.append("Description should be added ")

    if len(errors) > 0:
        return templates.TemplateResponse(
            "create_country.html", {"request": request, "errors": errors}
        )

    # retrive the token from the cookie.
    # the form title and browser data are send

    try:
        token = request.cookies.get("access_token")
        if not token:
            errors.append("Create account or Login")
            return templates.TemplateResponse(
                "create_country.html", {"request": request, "errors": errors}
            )

        scheme, _, param = token.partition(" ")
        # now decoded the token because i need the payload
        # takes the email from the people who is owner of the post
        payload = jwt.decode(param, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
        email = payload.get("sub")
        # take ID from database that is associate with this email
        if email is None:
            errors.append("This user doesn't exist. Create account")
            return templates.TemplateResponse(
                "create_country.html", {"request": request, "errors": errors}
            )
        else:
            user = db.query(User).filter(User.email == email).first()
            if user is None:
                errors.append("You are not authenticated, Kindly Login")
                return templates.TemplateResponse(
                    "create_item.html", {"request": request, "errors": errors}
                )
            else:
                # create object of the class
                country = Country(
                    country_name=country_name,
                    capital=capital,
                    official_lang=official_lang,
                    area=area,
                    description=description,
                    user_creator_id=user.user_id,
                )
                db.add(country)
                db.commit()
                db.refresh(country)
                return responses.RedirectResponse(
                    f"/detail/{country.country_id}", status_code=status.HTTP_302_FOUND
                )
    except Exception as e:
        errors.append("Something went wrong")
        print(e)
        return templates.TemplateResponse(
            "create_country.html", {"request": request, "errors": errors}
        )
@router.post("/country/uploadfile/{country_id_pass}", tags=["countries"])
async def create_upload_file(
    country_id_pass: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    FILEPATH = "static/images/"
    filename = file.filename
    # example test.png
    extension = filename.split(".")[1]

    if extension not in ["png", 'jpg']:
        return {"status": "error", "detial" : "File extension not allowed to upload"}
    
    #./static/images/"ududdj45.png
    token_name = secrets.token_hex(10)+"."+extension
    #generate info
    generated_name = FILEPATH + token_name
    file_content = await file.read()

    with open(generated_name, "wb") as file:
        file.write(file_content)

    #scallinf images by pillow
    img = Image.open(generated_name)
    img = img.resize(size = (200,200))
    img.save(generated_name)

    file.close()

    #get contry details
    country = db.query(Country).filter(Country.country_id == country_id_pass).first()
    

    if not country:
        return {"status": "error", "detail": "Country does not exist"}

    owner =  country.user_creator_id
    #check if right persone
    if owner != country.user_creator_id :
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Not authenticated to perform this action",
        )
    country.country_image = token_name
    db.commit()
    file_url = "localhost:8000" + generated_name[1:]
    return {"status": "ok", "filename": file_url}



@router.get("/update_delete_country")
def delete_country_show_list(request: Request, db: Session = Depends(get_db)):
    # fetch the token I need data from particular user
    token = request.cookies.get("access_token")
    errors = []
    if token is None:
        errors.append("You are not logged in")
        return templates.TemplateResponse(
            "update_delete.html", {"request": request, "errors": errors}
        )
    else:
        try:
            scheme, _, parm = token.partition(" ")
            payload = jwt.decode(parm, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
            email = payload.get("sub")
            user = db.query(User).filter(User.email == email).first()
            countries = (
                db.query(Country).filter(Country.user_creator_id == user.user_id).all()
            )
            return templates.TemplateResponse(
                "update_delete.html", {"request": request, "countires": countries}
            )
        except Exception as e:
            errors.append("Something is wrong")
            print(e)
            return templates.TemplateResponse(
                "update_delete.html", {"request": request, "errors": errors}
            )


@router.get("/search")
def search_country(request: Request, query: str = "", db: Session = Depends(get_db)):
    #the query parameter has to go from search box first and match contries
    countries = db.query(Country).filter(Country.country_name.contains(query)).all()
    return templates.TemplateResponse(
        "home.html", {"request": request, "countries": countries})
