from pydantic import BaseModel


class ExchangeDto(BaseModel):
    rates: dict[str, float]
