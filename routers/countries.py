from fastapi import APIRouter, Depends, HTTPException, status
from models import Country, User
from schemas import CountryCreate, ShowCountry, CountryUpdate
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from fastapi.encoders import jsonable_encoder
from routers.login import oauth2_scheme
from jose import jwt
from config import setting

router = APIRouter()

def get_user_from_token(db, token):
    #this is to decoded the token and it is return as payload data
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
        user = db.query(User).filter(User.email==username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
    return user

   
    
@router.post('/country', tags=['countries'], response_model=ShowCountry)
#user pass data the same like schema and pass them to modeltable
#adding token to check if the user is authenticated so ontly particular user can add country
def create_country(country: CountryCreate, db: Session = Depends(get_db), token: str=Depends(oauth2_scheme)):
    #country: CountryCreate this is schema user pass schema
    #this goes from database model countryn
    #this is to decoded the token and it is return as payload data
    user = get_user_from_token(db, token)
        # Create a new country using the Pydantic model's attributes
    new_country = Country(
        country_name=country.country_name,
        capital=country.capital,
        official_lang=country.official_lang, 
        area = country.area,
        description=country.description,
        user_creator_id=user.user_id
        )

    db.add(new_country)
    db.commit()
    db.refresh(new_country)
    return new_country
    # except Exception as e:
    #     # Handle any exceptions that occur during database operations
    #     db.rollback()
    #     raise HTTPException(status_code=500, detail="Internal Server Error")



#order metter in fasapi. 
# It goes line by line from the first and check for country/all
#when i have id fist then it will go to this and run but we are passing all so with this 
# because already pass in fisrt try it wont go farther
@router.get('/country/all', tags=['countries'], response_model=List[ShowCountry]) #response_model=ShowCountry it expected list of itmes and in showcountry I have for one element
def get_all_countries(db:Session = Depends(get_db)):
    all_countries = db.query(Country).all()
    return all_countries



#passing in path parameter router the id of the element what we want to read
@router.get('/country/{country_id_pass}', tags=['countries'], response_model=ShowCountry)
def get_country_by_id(country_id_pass: int, db: Session = Depends(get_db)): #i will need db because I get the id from db
    # I have to query data
    country = db.query(Country).filter(Country.country_id==country_id_pass).first() #country_id_pass that is what user pass into url
    if not country:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country does not exist. Create it")
    return country



@router.put('/country/update/{country_id_pass}', tags=['countries'])
#here is what we pass
def update_country_by_id(country_id_pass: int, country_update: CountryUpdate,
                          db: Session = Depends(get_db), token:str=Depends(oauth2_scheme)):
    user = get_user_from_token(db, token)
    
    existing_country = db.query(Country).filter(Country.country_id==country_id_pass)
    if not existing_country.first():
        return {"message" : f"No details exists for Country ID {country_id_pass}"}
    if existing_country().user_creator_id == user.user_id:
        #update key word use dictionary as an input
        # the country_update is pydentic schema and I have to convert to it jesonable_encoder
        #you can use magic method like existing_country.update(country_update.__dict__)
        existing_country.update(jsonable_encoder(country_update))
        # print(country_update)
        # print(jsonable_encoder(country_update))
        db.commit()
        return {"message" : f"Detail for Country ID {country_id_pass} has been sucessfully update it."}
    else:
        return {"message": "You are not authorized"}



@router.delete('/country/delete/{country_id_pass}', tags=['countries'])      
def delete_country_by_id(country_id_pass : int, db: Session = Depends(get_db), 
                         token:str=Depends(oauth2_scheme)):
    user = get_user_from_token(db, token)
    delete_country = db.query(Country).filter(Country.country_id==country_id_pass)
    if not delete_country.first():
        return {"message" : f"This country ID {country_id_pass} does not exist. Create one first"}
    if delete_country.first().user_creator_id == user.user_id:
        delete_country.delete()
        db.commit()
        return {"message": f"You deleted the country ID {country_id_pass}"}
    else:
        return {"message": "You are not authorized"}
    
   