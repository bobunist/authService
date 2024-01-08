from app.models.user import User
from app.repositories.repo import Repository


class UserRepository(Repository):
    model = User
