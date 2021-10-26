from fastapi import APIRouter

from app import crud, models, schemas

router = APIRouter()

router.get("/authors")
def read_author():
    pass

router.post("/authors")
def create_author():
    pass

router.put("/authors")
def update_author():
    pass

router.delete("/authors")
def delete_author():
    pass
