from typing import List

from pydantic import BaseModel


class Roles(BaseModel):
    roles: List["str"]

