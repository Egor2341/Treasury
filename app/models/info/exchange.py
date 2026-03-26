from pydantic import BaseModel


class ExchangeDto(BaseModel):
    usd: float
    eur: float
    cny: float