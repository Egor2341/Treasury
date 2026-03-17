from typing import List

from pydantic import BaseModel


class Categories(BaseModel):
    categories: List[str]
