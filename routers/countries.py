from fastapi import APIRouter, Depends, HTTPException, status
from models import Country
from schemas import CountryCreate, ShowCountry, CountryUpdate
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from fastapi.encoders import jsonable_encoder

router = APIRouter()


#the tag name it is kind of a folder for routers
@router.get('/countries', tags=['countries'])
def get_countires():
    return "Hello countries"

   
    
@router.post('/country', tags=['countries'], response_model=ShowCountry)
#user pass data the same like schema and pass them to modeltable
def create_country(country: CountryCreate, db: Session = Depends(get_db)):
    #country: CountryCreate this is schema user pass schema
    #this goes from database model countryn

        # Create a new country using the Pydantic model's attributes
    new_country = Country(
        country_name=country.country_name,
        capital=country.capital,
        official_lang=country.official_lang, 
        description=country.description,
        user_creator_id=country.user_creator_id
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
def update_country_by_id(country_id_pass: int, country_update: CountryUpdate, db: Session = Depends(get_db)):
    existing_country = db.query(Country).filter(Country.country_id==country_id_pass)
    if not existing_country.first():
        return {"message" : f"No details exists for Country ID {country_id_pass}"}
    else: 
        #update key word use dictionary as an input
        # the country_update is pydentic schema and I have to convert to it jesonable_encoder
        existing_country.update(jsonable_encoder(country_update))
        # print(country_update)
        # print(jsonable_encoder(country_update))
        db.commit()
        return {"message" : f"Detail for Country ID {country_id_pass} has been sucessfully update it."}
       
