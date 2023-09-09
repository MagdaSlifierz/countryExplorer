from fastapi import APIRouter, Depends, HTTPException, status
from models import Country
from schemas import CountryCreate, ShowCountry
from sqlalchemy.orm import Session
from database import get_db


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

#passing in path parameter router the id of the element what we want to read
@router.get('/country/{country_id_pass}', tags=['countries'], response_model=ShowCountry)
def get_country_by_id(country_id_pass: int, db: Session = Depends(get_db)): #i will need db because I get the id from db
    # I have to query data
    country = db.query(Country).filter(Country.country_id==country_id_pass).first() #country_id_pass that is what user pass into url
    if not country:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country does not exist. Create it")
    return country
    