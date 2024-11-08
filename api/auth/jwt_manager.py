from typing import Any

import jwt

from api.auth.jwt_settings import JWTSettings
from api.models.api.user_credentials import UserCredentials


class JWTManager:
    def __init__(self, jwt_settings: JWTSettings):
        self.__jwt_settings = jwt_settings

    def encode(self, user_id: int):
        return jwt.encode(
            payload=UserCredentials(id=user_id).model_dump(),
            key=self.__jwt_settings.secret,
            alg=self.__jwt_settings.algoritm,
        )

    def decode(self, encoded_jwt: str) -> Any:
        try:
            return jwt.decode(
                encoded_jwt,
                key=self.__jwt_settings.secret,
                algorithms=[self.__jwt_settings.algoritm],
            )

        except:
            return None
