from fastapi import FastAPI
from config import setting
from database import engine
from models import Base
from schemas import UserCreate


#that's the connection to database
Base.metadata.create_all(bind=engine)

#to do not have default name in docs I can specify them by routs. like folder

tags = [
    {
        "name": "user",
        "description":  "Routes related to user"
    },
    {
        "name": "countries",
        "description": "Routes related to description"
    }

]

#updating metadata information title THIS IS HARDCODED VERSION
#description_app = """
# Learn about the countires around the world"""
#
# app = FastAPI(title="Country Explorer",
#               description=description_app, 
#               contact = {
#                   "name": "Magdalena Slifierz"
#               }, openapi_tags=tags)

app = FastAPI(title = setting.TITLE, 
              version=setting.VERSION, 
              description= setting.DESCRIPTION,
              contact={ "name": setting.NAME} )


#the tag name it is kind of a folder for routers
@app.get('/user', tags=['user'])
def get_user():
    return "Hello user"

@app.get('/countries', tags=['countries'])
def get_countires():
    return "Hello countries"

@app.get('/getenvvar', tags=['congig'])
def get_evnars():
    return {"database": setting.DATABASE_URL}

@app.post('/users', tags=['user'])
def create_user(user: UserCreate): #accept data from the user using the schema user pass data
    print(user.email)
    print(user.password)