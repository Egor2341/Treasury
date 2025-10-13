from pydantic import BaseModel, EmailStr, SecretStr


class Login(BaseModel):
    email: EmailStr
    password: SecretStr