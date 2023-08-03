"""

Rather to have hard coded part of setting. 
Better is to use the class and pass it as argument

"""
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


class Settings:
    TITLE = "Country Explorer"
    VERSION = "0.1.0"
    DESCRIPTION = """
            ## Learn about the countires around the world """
    NAME = "Magdalena Slifierz"

    #pulling from loaddotev 
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER=os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT=os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB=os.getenv("POSTGRES_DB", "mydb")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


#create a object from the class
setting = Settings()