from fastapi import APIRouter


router = APIRouter()


#the tag name it is kind of a folder for routers
@router.get('/countries', tags=['countries'])
def get_countires():
    return "Hello countries"



