from pydantic import BaseModel, Field


class EditDto(BaseModel):
    uuid: str
    name: str = Field(..., min_length=1, max_length=64, description="min = 1, max = 64")
