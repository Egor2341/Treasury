from typing import List

from pydantic import BaseModel


class UserInfo(BaseModel):
    email: str
    roles: List[str]
