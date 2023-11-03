from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from models import Country, User
from schemas import CountryCreate, ShowCountry, CountryUpdate
from sqlalchemy.orm import Session
from database import get_db
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from routers.login import oauth2_scheme
from jose import jwt
from config import setting
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image
router = APIRouter()

# static file setup 

def get_user_from_token(db, token):
    # this is to decoded the token and it is return as payload data
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to verify credentials",
            )
        user = db.query(User).filter(User.email == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to verify credentials",
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to verify credentials",
        )
    return user


@router.post("/country", tags=["countries"], response_model=ShowCountry)
# user pass data the same like schema and pass them to modeltable
# adding token to check if the user is authenticated so ontly particular user can add country
def create_country(
    country: CountryCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    file: UploadFile = File(None),
):
    # country: CountryCreate this is schema user pass schema
    # this goes from database model countryn
    # this is to decoded the token and it is return as payload data
    user = get_user_from_token(db, token)
    # Create a new country using the Pydantic model's attributes
    new_country = Country(
        country_name=country.country_name,
        capital=country.capital,
        official_lang=country.official_lang,
        area=country.area,
        description=country.description,
        user_creator_id=user.user_id,
    )

    if file:
        extension = file.filename.split("."[-1])
        if extension not in ["png", "jpg"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File extension not allowed for image upload",
            )
        generated_name = f"images/{secrets.token_hex(10)}.{extension}"
        with open(generated_name, "wb") as image_file:
            image_file.write(file.file.read())
        new_country.country_image = generated_name

    db.add(new_country)
    db.commit()
    db.refresh(new_country)
    return new_country
    # except Exception as e:
    #     # Handle any exceptions that occur during database operations
    #     db.rollback()
    #     raise HTTPException(status_code=500, detail="Internal Server Error")



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
    # file_url = "localhost:8000" + generated_name[1:]
    file_url = "/static/images/" + token_name
    return {"status": "ok", "filename": file_url}




@router.get("/country/autocomplete")
def autocomplete(term: Optional[str], db: Session=Depends(get_db)): # take argument that user type term
    countries = db.query(Country).filter(Country.country_name.contains(term)).all()
    #list sugestions will show the output
    sugestions = []
    for country in countries:
        sugestions.append(country.country_name)
    return sugestions


# order metter in fasapi.
# It goes line by line from the first and check for country/all
# when i have id fist then it will go to this and run but we are passing all so with this
# because already pass in fisrt try it wont go farther
@router.get(
    "/country/all", tags=["countries"], response_model=List[ShowCountry]
)  # response_model=ShowCountry it expected list of itmes and in showcountry I have for one element
def get_all_countries(db: Session = Depends(get_db)):
    all_countries = db.query(Country).all()
    return all_countries


# passing in path parameter router the id of the element what we want to read
@router.get(
    "/country/{country_id_pass}", tags=["countries"], response_model=ShowCountry
)
def get_country_by_id(
    country_id_pass: int, db: Session = Depends(get_db)
):  # i will need db because I get the id from db
    # I have to query data
    country = (
        db.query(Country).filter(Country.country_id == country_id_pass).first()
    )  # country_id_pass that is what user pass into url
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country does not exist. Create it",
        )
    return country


@router.put("/country/update/{country_id_pass}", tags=["countries"])
# here is what we pass
def update_country_by_id(
    country_id_pass: int,
    country_update: CountryUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    user = get_user_from_token(db, token)

    existing_country = db.query(Country).filter(Country.country_id == country_id_pass)
    if not existing_country.first():
        return {"message": f"No details exists for Country ID {country_id_pass}"}
    if existing_country.first().user_creator_id == user.user_id:
        # update key word use dictionary as an input
        # the country_update is pydentic schema and I have to convert to it jesonable_encoder
        # you can use magic method like existing_country.update(country_update.__dict__)
        existing_country.update(jsonable_encoder(country_update))
        # print(country_update)
        # print(jsonable_encoder(country_update))
        db.commit()
        return {
            "message": f"Detail for Country ID {country_id_pass} has been sucessfully update it."
        }
    else:
        return {"message": "You are not authorized"}


@router.delete("/country/delete/{country_id_pass}", tags=["countries"])
def delete_country_by_id(
    country_id_pass: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    user = get_user_from_token(db, token)
    delete_country = db.query(Country).filter(Country.country_id == country_id_pass)
    if not delete_country.first():
        return {
            "message": f"This country ID {country_id_pass} does not exist. Create one first"
        }
    if delete_country.first().user_creator_id == user.user_id:
        delete_country.delete()
        db.commit()
        return {"message": f"You deleted the country ID {country_id_pass}"}
    else:
        return {"message": "You are not authorized"}
