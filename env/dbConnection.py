import mariadb
from fastapi import FastAPI

app = FastAPI()
db_connection = None

@app.on_event("startup")
async def startup():
    global db_connection
    db_connection = await mariadb.connect(
        host="localhost",
        port=3300,
        user="root",
        password="ziye245680",
        database="harone_crm"
    )

@app.on_event("shutdown")
async def shutdown():
    if db_connection:
        await db_connection.close()

def harone_crm_db():
    return db_connection