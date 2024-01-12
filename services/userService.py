from fastapi.responses import JSONResponse
from env.dbConnection import get_database_connection
from mysql.connector import Error

def get_all_users():
    try:
        with get_database_connection().cursor() as cursor:
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