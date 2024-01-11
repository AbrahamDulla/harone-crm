from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from env.dbConnection import harone_crm_db
app = FastAPI()
views = Jinja2Templates(directory="views")
# from .routes.userRoute import router as user_router


@app.get('/')
async def home(request: Request):
    return views.TemplateResponse("home.html", {"request": request, "first_message": "Abraham"})