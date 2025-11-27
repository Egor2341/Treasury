from pydantic import BaseModel, Field


class Edit(BaseModel):
    type: str
    old_name: str = Field(..., min_length=1, max_length=64, description="min = 1, max = 64")
    new_name: str = Field(..., min_length=1, max_length=64, description="min = 1, max = 64")