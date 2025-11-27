from pydantic import BaseModel, EmailStr, SecretStr, Field


class Register(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=32, description="min = 1, max = 32")
    password: SecretStr