from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from env.dbConnection import harone_crm_db
app = FastAPI()
views = Jinja2Templates(directory="views")

from services.userService import (get_user, get_users, create_user, update_user, delete_user)


@app.get('/')
async def home(request: Request):
    return views.TemplateResponse("home.html", {"request": request, "first_message": "Abraham"})

@app.get("/abrelo")
def ab(request: Request):
    return {"message": "abraham"}
        

# users routes
@app.get("/users")
def read_users(db = Depends(harone_crm_db)):
    return get_users(db)

@app.get("/users/{user_id}")
def read_user(user_id: int, db = Depends(harone_crm_db)):
    return get_user(db, user_id)

@app.post("/users")
def create_user(user_data, db = Depends(harone_crm_db)):
    return create_user(db, user_data)

@app.put("/users/{user_id}")
def update_user(user_id: int, user_data, db = Depends(harone_crm_db)):
    return update_user(db, user_id, user_data)

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db = Depends(harone_crm_db)):
    delete_user(db, user_id)
    return {"message": "User deleted"}