class AuthService:
    def __init__(self):
        self.users = {
            "admin": "password",
            "user1": "pass123",
        }

    def authenticate_user(self, username: str, password: str):
        if username in self.users and self.users[username] == password:
            return True
        return False