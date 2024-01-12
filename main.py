from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from env.dbConnection import get_database_connection, close_database_connection
from services.userService import (get_user, get_users, create_user, update_user, delete_user)
from mysql.connector import Error

app = FastAPI()
views = Jinja2Templates(directory="views")

@app.on_event("startup")
async def startup():
    app.db_connection = get_database_connection()

@app.on_event("shutdown")
async def shutdown():
    close_database_connection(app.db_connection)

@app.get('/')
async def redirect_to_login():
    return RedirectResponse(url="/login")

@app.get('/login')
async def login(request: Request):
    return views.TemplateResponse("login.html", {"request": request})

@app.get('/register')
async def register(request: Request):
    return views.TemplateResponse("web/register.html", {"request": request})

@app.get('/request')
async def request(request: Request):
    return views.TemplateResponse("web/request.html", {"request": request})

@app.get('/crm')
async def dashboard(request: Request):
    return views.TemplateResponse("crm/dashboard.html", {"request": request})

@app.get('/crm/login')
async def crmLogin(request: Request):
    return views.TemplateResponse("crm/login.html", {"request": request})

@app.get("/abrelo")
def ab(request: Request):
    return {"message": "abraham"}

# users routes
@app.get("/users")
def read_users(db=Depends(get_database_connection)):
    return get_users(db)

@app.get("/users/{user_id}")
def read_user(user_id: int, db=Depends(get_database_connection)):
    return get_user(db, user_id)

@app.post("/users")
def create_user(user_data, db=Depends(get_database_connection)):
    return create_user(db, user_data)

@app.put("/users/{user_id}")
def update_user(user_id: int, user_data, db=Depends(get_database_connection)):
    return update_user(db, user_id, user_data)

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db=Depends(get_database_connection)):
    delete_user(db, user_id)
    return {"message": "User deleted"}

@app.get("/userrr")
async def get_users():
    try:
        with app.db_connection.cursor() as cursor:
            query = "SELECT * FROM users"
            cursor.execute(query)
            result = cursor.fetchall()

            users = []
            for row in result:
                user = {
                    "id": row[0],
                    "name": row[1],
                    "email": row[2]
                }
                users.append(user)

            return JSONResponse(content=users)
    except Error as e:
        return JSONResponse(content={"error": str(e)})
