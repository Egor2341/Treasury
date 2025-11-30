from pydantic import BaseModel, EmailStr, SecretStr


class Register(BaseModel):
    email: EmailStr
    password: SecretStr