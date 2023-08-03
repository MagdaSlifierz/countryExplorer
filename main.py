from fastapi import FastAPI


description_app = """
## Learn about the countires around the world
"""
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

#updating metadata information title
app = FastAPI(title="Country Explorer",
              description=description_app, 
              contact = {
                  "name": "Magdalena Slifierz"
              }, openapi_tags=tags)

#the tag name it is kind of a folder for routers
@app.get('/user/', tags=['user'])
def get_user():
    return "Hello user"

@app.get('/countries', tags=['countries'])
def get_countires():
    return "Hello countries"