from typing import Any

from jwt import JWT

from api.auth.jwt_settings import JWTSettings


class JWTManager:
    def __init__(self, jwt_settings: JWTSettings):
        self.__jwt_settings = jwt_settings

    def encode(self, user_id: int):
        return JWT.encode(
            payload={"user_id": user_id},
            key=self.__jwt_settings.secret,
            alg=self.__jwt_settings.algoritm,
        )

    def decode(self, encoded_jwt: str) -> Any:
        try:
            return JWT.decode(
                encoded_jwt,
                key=self.__jwt_settings.secret,
                algorithms=[self.__jwt_settings.algoritm],
            )
        except:
            return None
