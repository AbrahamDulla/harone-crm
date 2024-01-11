from fastapi import APIRouter, Depends
from ..env.dbConnection import harone_crm_db
from ..services import (
    get_user, get_users, create_user, update_user, delete_user
)

router = APIRouter()

@router.get("/users/{user_id}")
def read_user(user_id: int, db = Depends(harone_crm_db)):
    return get_user(db, user_id)

@router.get("/users")
def read_users(db = Depends(harone_crm_db)):
    return get_users(db)

@router.post("/users")
def create_user(user_data, db = Depends(harone_crm_db)):
    return create_user(db, user_data)

@router.put("/users/{user_id}")
def update_user(user_id: int, user_data, db = Depends(harone_crm_db)):
    return update_user(db, user_id, user_data)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db = Depends(harone_crm_db)):
    delete_user(db, user_id)
    return {"message": "User deleted"}