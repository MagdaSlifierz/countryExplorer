from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from sqlalchemy.orm import relationship


# we can update the schema, we don;t have to delete it every time
# created two tables
class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(225))
    last_name = Column(String)
    email = Column(String(225), unique=True, index=True, nullable=False)
    password = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)

    # Define a relationship with the 'Country' model
    # Use 'Country.creator_user' to reference the back_populates attribute  
    country = relationship("Country", back_populates="creator_user")



class Country(Base):
    __tablename__ = 'countries'

    country_id = Column(Integer, primary_key=True, index=True)
    country_name = Column(String,  nullable=False)
    capital = Column(String)
    official_lang = Column(String)
    area = Column(String)
    description = Column(String)
    
    user_creator_id = Column(Integer, ForeignKey('users.user_id'))

    #create a relationship between 2 class
    #back_populates or back_references it will still both work.
    #can be also without it but with it the fild will be updated in any tables 
    
    creator_user = relationship("User", back_populates="country" )