from pydantic import BaseModel, Field, ConfigDict


class CategoryDto(BaseModel):
    name: str = Field(..., min_length=1, max_length=64, description="min = 1, max = 64")
    type: str