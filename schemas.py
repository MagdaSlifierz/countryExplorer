from pydantic import EmailStr
from pydantic import BaseModel

class User(BaseModel):
    user_id : int
    first_name : str
    last_name : str
    email : EmailStr
    password : str


class Country(BaseModel):
    country_name : str
    capital : str
    official_flag: str
    description : str