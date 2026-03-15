from typing import List

from pydantic import BaseModel


class ListOneTypeCategories(BaseModel):
    categories: List[str]
    uuids: List[str]
