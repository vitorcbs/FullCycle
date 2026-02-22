from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register_user(self, email, name, password_hash):
        return self.repo.create(email, name, password_hash)