from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

name = "python"

@app.get('/')
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "first_message": f"I Love {name}"})