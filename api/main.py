import logging
from fastapi import FastAPI
from starlette.responses import JSONResponse

from api.errors import UserNotFoundError
from api.routers.friends import FriendsRouter
from api.routers.users import UsersRouter
from api.storage.friends import FriendStorage
from api.storage.users import UserStorage


logging.basicConfig(
    filename='log_app.log',
    level=logging.DEBUG,
    format="%(levelname)s: [%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} - %(message)s",
)


class App(FastAPI):
    def __init__(self, users_router: UsersRouter, friends_router: FriendsRouter):
        super().__init__()
        self.include_router(users_router)
        self.include_router(friends_router)
        self.exception_handler(UserNotFoundError)(self.user_not_found_handler_error)

    async def user_not_found_handler_error(self, request, exc):
        return JSONResponse(str(exc), status_code=404)


user_storage = UserStorage()
users_router = UsersRouter(user_storage=user_storage)
friends_storage = FriendStorage()
friends_router = FriendsRouter(friends_storage=friends_storage)
app = App(users_router=users_router, friends_router=friends_router)
