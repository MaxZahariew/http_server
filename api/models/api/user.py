from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: int = 0
    name: str
    age: int
    about: str
    email: str
    password: str
