from fastapi import APIRouter
from fastapi import Response
import bcrypt

from api.models.api.login_request import LoginRequest
from api.auth.jwt_manager import JWTManager
from api.auth.jwt_settings import JWTSettings
from api.storage.users import UserStorage
from api.errors import NotAuthenticatedError

import logging


logger = logging.getLogger(__name__)


class LoginRouter(APIRouter):

    def __init__(
        self,
        user_storage: UserStorage,
        jwt_manager: JWTManager,
        jwt_setting: JWTSettings,
    ):
        super().__init__()
        self.tags = ["login"]

        @self.post("/login/")
        async def login(login_request: LoginRequest, response: Response):
            user = user_storage.find_user(login_request.email)
            print(f"Entered Password: {login_request.password}")
            print(f"Stored Hashed Password: {user.password}")
            if bcrypt.checkpw(login_request.password.encode(),
                              user.password.encode()):
                response.set_cookie(
                    key=jwt_setting.session_cookie_key,
                    value=jwt_manager.encode(user.id),
                )
                return {"message": f"User {user} was authenticated"}
            logger.info("User entered wrong password")
            raise NotAuthenticatedError()
