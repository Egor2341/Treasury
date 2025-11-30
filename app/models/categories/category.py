from pydantic import BaseModel, Field, ConfigDict


class CategoryDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(..., min_length=1, max_length=64, description="min = 1, max = 64")
    type: str