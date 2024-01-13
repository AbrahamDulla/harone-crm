class AuthService:
    async def authenticate_user(self, db, name: str, password: str):
        try:
            with db.cursor() as cursor:
                query = "SELECT password FROM users WHERE name = %s"
                cursor.execute(query, (name.lower(),))
                result = cursor.fetchone()

                if result and result[0] == password:
                    return True
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False
