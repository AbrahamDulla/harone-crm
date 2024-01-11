from fastapi import HTTPException

def get_user(db, user_id: int):
    query = "SELECT * FROM users WHERE id = :user_id"
    result = db.execute(query, {"user_id": user_id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(result)

def get_users(db):
    query = "SELECT * FROM users"
    results = db.execute(query).fetchall()
    return [dict(result) for result in results]

def create_user(db, user_data):
    query = "INSERT INTO users (username, email, password) VALUES (:username, :email, :password)"
    db.execute(query, user_data)
    db.commit()
    user_id = db.execute("SELECT LAST_INSERT_ID()").scalar()
    return get_user(db, user_id)

def update_user(db, user_id: int, user_data):
    query = "UPDATE users SET username = :username, email = :email, password = :password WHERE id = :user_id"
    user_data["user_id"] = user_id
    result = db.execute(query, user_data)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    db.commit()
    return get_user(db, user_id)

def delete_user(db, user_id: int):
    query = "DELETE FROM users WHERE id = :user_id"
    result = db.execute(query, {"user_id": user_id})
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    db.commit()