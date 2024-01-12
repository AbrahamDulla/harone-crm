class AuthService:
    def __init__(self):
        self.users = {
            "abraham": "12341234",
            "surafel": "12341234",
        }

    async def authenticate_user(self, username: str, password: str):
        # Ensure the following lines are indented correctly
        username = username.lower()  # This line should be indented inside the function
        if username in (user.lower() for user in self.users) and self.users[username] == password:
            return True
        return False
