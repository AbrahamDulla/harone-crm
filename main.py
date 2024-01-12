from fastapi import FastAPI, Depends, Request, HTTPException, status, Query, Response, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing_extensions import Annotated
from env.dbConnection import get_database_connection, close_database_connection
from services.userService import get_all_users
from mysql.connector import Error
from services.auth_service import AuthService
from pydantic import BaseModel
from typing import Optional
from random import randrange

auth_service = AuthService()
security = HTTPBasic()
app = FastAPI()
views = Jinja2Templates(directory="views")


class Customer(BaseModel):
    company_name: str
    company_email: str
    business_address: str
    industry: str


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


@app.post('/request')
async def request_page(request: Request):
    return views.TemplateResponse("web/request.html", {"request": request})

@app.get('/crm')
async def dashboard(request: Request):
    return views.TemplateResponse("crm/dashboard.html", {"request": request})




@app.get("/users")
def read_users(db=Depends(get_database_connection)):
    return get_all_users()

def get_user_by_name(name: str, db):
    try:
        with db.cursor(dictionary=True) as cursor:
            query = "SELECT * FROM users WHERE name = %s"
            cursor.execute(query, (name,))
            return cursor.fetchone() 
    except Error as e:
        print(f"Error fetching user: {e}")
        return None


@app.post("/login")
async def login_post(request: Request, username: str = Form(...), password: str = Form(...), db=Depends(get_database_connection)):
    

    if await auth_service.authenticate_user(username, password):
        user = get_user_by_name(username, db)
        if user:
            role = user['role'] 
            print("Role:", role)
            print("User:", user)
            
            if role == "admin":
                response = RedirectResponse(url="/crm", status_code=status.HTTP_303_SEE_OTHER)
                return response
            elif role == "customer":
                return RedirectResponse(url="/request")
            else:
                return views.TemplateResponse("login.html", {"request": request, "error_message": "Invalid role"})
        else:
            return views.TemplateResponse("login.html", {"request": request, "error_message": "User not found"})
    else:
        return views.TemplateResponse("login.html", {"request": request, "error_message": "Invalid username or password"})


from fastapi.responses import JSONResponse

@app.post("/send/request", status_code=status.HTTP_201_CREATED)
async def create_post(request: Request, db=Depends(get_database_connection)):
    form = await request.form()
    customer = Customer(
        company_name=form.get("company_name"),
        company_email=form.get("company_email"),
        business_address=form.get("business_address"),
        industry=form.get("industry")
    )
    try:
        with db.cursor() as cursor:
            query = "INSERT INTO customers (company_name, company_email, business_address, industry) VALUES (%s, %s, %s, %s)"
            values = (customer.company_name, customer.company_email, customer.business_address, customer.industry)
            cursor.execute(query, values)
            db.commit()
            
            request_id = cursor.lastrowid
            return JSONResponse(content={"message": customer.company_name + " Requested successfully", "request_id": request_id})
    except Error as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

