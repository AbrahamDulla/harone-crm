from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing_extensions import Annotated
from env.dbConnection import get_database_connection, close_database_connection
from services.userService import get_all_users
from mysql.connector import Error
from services.auth_service import AuthService

auth_service = AuthService()
security = HTTPBasic()
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
async def request_page(request: Request):
    return views.TemplateResponse("web/request.html", {"request": request})

@app.get('/crm')
async def dashboard(request: Request):
    return views.TemplateResponse("crm/dashboard.html", {"request": request})


@app.post("/login")
async def login_post(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    # username = credentials.username
    # password = credentials.password
    username = "admin"
    password = "password"
    role = "customer"

    print("Received credentials:", credentials)
    print("Username:", username)
    print("Password:", password)

    if await auth_service.authenticate_user(username, password):
        if role == "admin":
                return views.TemplateResponse("crm/dashboard.html", {"request": request, "username": username})
        elif role == "customer":
                return views.TemplateResponse("web/request.html", {"request": request})
        else:
                return views.TemplateResponse("login.html", {"request": request, "error_message": "Invalid role"})
    else:
        # return {"username": credentials.username, "password": credentials.password}
        return views.TemplateResponse("login.html", {"request": request, "error_message": "Invalid username or password"})

# users routes
@app.get("/users")
def read_users(db=Depends(get_database_connection)):
    return get_all_users()