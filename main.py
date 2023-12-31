from fastapi import FastAPI
from config import setting
from database import engine
from models import Base
from routers import users, countries, login
from webapp.routers import country as web_country
from webapp.routers import user as web_user
from webapp.routers import auth as web_auth
from fastapi.staticfiles import StaticFiles


# that's the connection to database
# Base.metadata.create_all(bind=engine) I use alabemic migrations so I dont neet that

# to do not have default name in docs I can specify them by routs. like folder

tags = [
    {"name": "user", "description": "Routes related to user"},
    {"name": "countries", "description": "Routes related to description"},
]

# updating metadata information title THIS IS HARDCODED VERSION
# description_app = """
# Learn about the countires around the world"""
#
# app = FastAPI(title="Country Explorer",
#               description=description_app,
#               contact = {
#                   "name": "Magdalena Slifierz"
#               }, openapi_tags=tags)

app = FastAPI(
    title=setting.TITLE,
    version=setting.VERSION,
    description=setting.DESCRIPTION,
    contact={"name": setting.NAME},
)

# for static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# this is to include routers
app.include_router(users.router)
app.include_router(countries.router)
app.include_router(login.router)
app.include_router(web_country.router)
app.include_router(web_user.router)
app.include_router(web_auth.router)
