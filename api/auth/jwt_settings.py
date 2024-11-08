from pydantic_settings import BaseSettings
from pydantic import Field

from datetime import timedelta


class JWTSettings(BaseSettings):
    secret: str = "IMaxZah"
    algoritm: str = "HS256"
    session_cookie_key: str = "session"
    session_cookie_expires: timedelta = timedelta(minutes=42)
    use_bearer: bool = Field(
        False,
        description="used to switch between cookie or bearer-header authentication.",
    )

    class Config:
        env_prefix = "JWT"
