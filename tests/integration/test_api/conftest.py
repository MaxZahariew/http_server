import pytest
from starlette.testclient import TestClient

from api.main import App
from api.auth.jwt_manager import JWTManager
from api.auth.jwt_settings import JWTSettings
from api.routers.friends import FriendsRouter
from api.routers.login import LoginRouter
from api.routers.users import UsersRouter
from api.routers.middlewares.jwt import JWTBearer, JWTMiddleware
from api.storage.friends import FriendStorage
from api.storage.users import UserStorage


@pytest.fixture()
def user_storage() -> UserStorage:
    return UserStorage()


@pytest.fixture()
def friends_storage() -> FriendStorage:
    return FriendStorage()


@pytest.fixture()
def users_router(user_storage: UserStorage) -> UsersRouter:
    return UsersRouter(user_storage=user_storage)


@pytest.fixture()
def friends_router(friends_storage: FriendStorage) -> FriendsRouter:
    return FriendsRouter(friends_storage=friends_storage)

@pytest.fixture()
def jwt_settings() -> JWTSettings:
    return JWTSettings()


@pytest.fixture()
def jwt_manager(jwt_settings: JWTSettings) -> JWTManager:
    return JWTManager(jwt_settings=jwt_settings)


@pytest.fixture()
def login_router(
    user_storage: UserStorage,
    jwt_manager: JWTManager,
    jwt_settings: JWTSettings,
) -> LoginRouter:
    return LoginRouter(
        user_storage=user_storage,
        jwt_manager=jwt_manager,
        jwt_setting=jwt_settings
    )



@pytest.fixture()
def app(users_router: UsersRouter,
        friends_router: FriendsRouter,
        login_router: LoginRouter
        ) -> App:
    return App(users_router=users_router,
               friends_router=friends_router,
               login_router=login_router,
               )


@pytest.fixture()
def client(app: App) -> TestClient:
    return TestClient(app)
