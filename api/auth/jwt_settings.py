from pydantic_settings import BaseSettings


class JWTSettings(BaseSettings):
    secret: str = "IMaxZah"
    algoritm: str = "HS256"
    session_cookie_key: str = "session"

    class Config:
        env_prefix = "JWT"