import enum
import logging
from typing import List, Any

from fastapi import HTTPException, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from api.auth.jwt_manager import JWTManager
from api.auth.jwt_settings import JWTSettings
from api.errors import NotAuthorzationError
from api.models.api.user_credentials import UserCredentials
from api.storage.users import UserStorage


logger = logging.getLogger(__name__)


class AuthGroup(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class JWTBearer(HTTPBearer):

    def __init__(self, jwt_manager: JWTManager, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.__jwt_manager = jwt_manager

    async def __call__(self, request: Request):
        # credentials: HTTPAuthorizationCredentials = await super(
        #     JWTBearer, self
        # ).__call__(request)
        # if credentials:
        #     if not credentials.scheme == "Bearer":
        #         raise HTTPException(
        #             status_code=403, detail="Invalid authentication scheme."
        #         )
        #     if not self.__jwt_manager.decode(credentials.credentials):
        #         raise HTTPException(
        #             status_code=403, detail="Invalid toketn on expired token"
        #         )
        #     return credentials.credentials
        # else:
        #     raise HTTPException(status_code=403, detail="Invalid authorization code")
        pass


class JWTCookie:
    """Gets credentials from token in cookie"""

    def __init__(self, jwt_manager: JWTManager, jwt_settinsg: JWTSettings):
        self.__jwt_manager = jwt_manager
        self.__jwt_settings = jwt_settinsg

    async def __call__(self, request: Request) -> UserCredentials:
        jwt_cookie = request.cookies.get(self.__jwt_settings.session_cookie_key)
        decoded_credentials = self.__jwt_manager.decode(jwt_cookie)
        if not decoded_credentials:
            raise HTTPException(
                status_code=403, detail="Invalid token or expired token"
            )
        logger.info("decoded credentials %s", decoded_credentials)
        return UserCredentials.parse_obj(decoded_credentials)


class JWTMiddleware:

    def __init__(
        self,
        jwt_manager: JWTManager,
        jwt_bearer: JWTBearer,
        jwt_cookie: JWTCookie,
        jwt_settings: JWTSettings,
        user_storage: UserStorage,
    ):
        self.__jwt_manager = jwt_manager
        self.__jwt_bearer = jwt_bearer
        self.__jwt_cookie = jwt_cookie
        self.__jwt_settings = jwt_settings
        self.__user_storage = user_storage

    async def _get_credentials(self, request: Request) -> UserCredentials:
        if self.__jwt_settings.use_bearer:
            logger.debug("getting credentials from token")
            method = self.__jwt_bearer
        else:
            logger.debug("getting credentials from bearer header")
            method = self.__jwt_cookie
        credentials = await method.__call__(request)
        logger.debug("got credentials %s", credentials)
        return credentials

    def _wrap_if_bearer(self, func):

        if self.__jwt_settings.use_bearer:

            class _Wrapper(HTTPBearer):
                async def __call__(_, request: Request) -> Response:
                    return await func(request)

            return _Wrapper()
        else:
            return func

    def get_user_credentials(self):
        return self._wrap_if_bearer(self._get_credentials)

    def get_user(self):
        async def __call__(request: Request) -> User:
            credentials = await self._get_credentials(request=request)
            return self._users_storage.get_user(credentials.id)

        return self._wrap_if_bearer(__call__)

    def ensure_has_rights(self, required_groups: List[AuthGroup]):
        async def __call__(request: Request) -> UserCredentials:
            credentials =  await self._get_credentials(request=request)
            if AuthGroup.ADMIN in required_groups:
                raise NotAuthorzationError()
            return "ok"

        return self._wrap_if_bearer(__call__)
