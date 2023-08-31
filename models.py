from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


# we can update the schema, we don;t have to delete it every time
# created two tables
class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, length=225)
    last_name = Column(String, length=225)
    email = Column(String, length=225, unique=True, index=True, nullable=False)
    password = Column(String, length=225, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)

    country = relationship("Country", back_populates="country_user")



class Country(Base):
    __tablename__ = 'countries'

    country_id = Column(Integer, primary_key=True, index=True)
    country_name = Column(String, length=225, nullable=False)
    capital = Column(String, length=225)
    official_lang = Column(String, length=225)
    description = Column(String, length=225)
    
    user_creator_id = Column(Integer, ForeignKey('users.user_id'))

    #create a relationship between 2 class
    #back_populates or back_references it will still both work.
    #can be also without it but with it the fild will be updated in any tables 
    
    creator_user = relationship("User", back_populates="country" )