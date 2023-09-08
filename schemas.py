from pydantic import EmailStr
from pydantic import BaseModel

class UserCreate(BaseModel):
    first_name : str
    last_name : str
    email : EmailStr
    password : str

class UserShow(BaseModel):
    first_name : str
    last_name : str
    email : EmailStr
    is_active: bool

    #it will output json response key-value pair. it should map our class usershow to key. 
    class Config:
        orm_mode=True


class CountryCreate(BaseModel):
    country_name : str
    capital : str
    official_lang: str
    description : str
    user_creator_id : int
    

class ShowCountry(BaseModel):
    country_name : str
    capital : str
    official_lang: str
    description : str

    class Config:
        orm_mode = True

        '''{
  "country_name": "Poland",
  "capital": "Warsaw",
  "official_lang": "Polish",
  "description": "Poland is located at the heart of the European continent"
}'''