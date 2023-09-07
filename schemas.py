from pydantic import EmailStr
from pydantic import BaseModel

class UserCreate(BaseModel):
    first_name : str
    last_name : str
    email : EmailStr
    password : str


class Country(BaseModel):
    country_name : str
    capital : str
    official_flag: str
    description : str