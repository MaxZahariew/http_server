from api.errors import UserNotFoundError
from api.models.user import User


class UserStorage:
    def __init__(self):
        self.__users = {}

    def __len__(self) -> int:
        return len(self.__users)

    def create_user(self, user: User) -> User:
        if user.id in self.__users:
            raise Exception(f"User in {user.id} already extists")

        self.__users[user.id] = user

        return user

    def get_users(self) -> list[User]:
        return [user for user in self.__users.values()]

    def get_user(self, id_: int) -> User:
        if id_ not in self.__users:
            raise UserNotFoundError(f"User {id_} was not found")

        return self.__users[id_]

    def update_user(self, id_: int, new_user: User) -> User:
        if id_ not in self.__users:
            raise UserNotFoundError(f"User {id_} was not found")

        self.__users[id_] = new_user
        return new_user
