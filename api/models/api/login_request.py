from pydantic import BaseModel
import bcrypt

class LoginRequest(BaseModel):
    email: str
    password: str
