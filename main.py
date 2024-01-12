from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from env.dbConnection import get_database_connection, close_database_connection
from services.userService import (get_all_users)
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


# users routes
@app.get("/users")
def read_users(db=Depends(get_database_connection)):
    return get_all_users()