import logging
from fastapi import FastAPI
from starlette.responses import JSONResponse

from api.errors import UserNotFoundError, NotAuthenticatedError, NotAuthorzationError
from api.auth.jwt_settings import JWTSettings
from api.auth.jwt_manager import JWTManager
from api.routers.friends import FriendsRouter
from api.routers.users import UsersRouter
from api.routers.login import LoginRouter
from api.routers.chat import ChatRouter
from api.storage.friends import FriendStorage
from api.storage.users import UserStorage
from api.routers.middlewares.jwt import JWTBearer, JWTCookie, JWTMiddleware


logging.basicConfig(
    filename="log_app.log",
    level=logging.DEBUG,
    format="%(levelname)s: [%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} - %(message)s",
)


class App(FastAPI):
    def __init__(
        self,
        users_router: UsersRouter,
        friends_router: FriendsRouter,
        login_router: LoginRouter,
        chat_router: ChatRouter,
    ):
        super().__init__()
        self.include_router(users_router)
        self.include_router(friends_router)
        self.include_router(login_router)
        self.include_router(chat_router)

        # self.exception_handler(UserNotFoundError)(self._user_not_found_handler_error)
        # self.exception_handler(NotAuthorzationError)(self._bad_auth_error)
        # self.exception_handler(NotAuthenticatedError)(self._bad_auth_error)
        # self.exception_handler(Exception)(self._server_error)

    async def user_not_found_handler_error(self, request, exc):
        return JSONResponse(str(exc), status_code=404)


user_storage = UserStorage()
friends_storage = FriendStorage()

jwt_settings = JWTSettings()
jwt_manager = JWTManager(jwt_settings=jwt_settings)
jwt_bearer = JWTBearer(jwt_manager=jwt_manager)
jwt_cookie = JWTCookie(jwt_manager=jwt_manager, jwt_settinsg=jwt_settings)
jwt_midleware = JWTMiddleware(
    jwt_manager=jwt_manager,
    jwt_bearer=jwt_bearer,
    jwt_cookie=jwt_cookie,
    jwt_settings=jwt_settings,
    user_storage=user_storage,

)


users_router = UsersRouter(user_storage=user_storage, jwt_midleware=jwt_midleware)
friends_router = FriendsRouter(friends_storage=friends_storage)
chat_router = ChatRouter(
    user_storage=user_storage,
    friends_storage=friends_storage,
    jwt_manager=jwt_manager,
    jwt_settings=jwt_settings,
    jwt_middleware=jwt_midleware
    )
login_router = LoginRouter(
    user_storage=user_storage,
    jwt_manager=jwt_manager,
    jwt_setting=jwt_settings,
)
chat_router = ChatRouter(
    user_storage=user_storage,
    friends_storage=friends_storage,
    jwt_manager=jwt_manager,
    jwt_settings=jwt_settings,
    jwt_middleware=jwt_midleware,
)

app = App(
    users_router=users_router,
    friends_router=friends_router,
    login_router=login_router,
    chat_router=chat_router
)
