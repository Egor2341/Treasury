from pydantic import BaseModel


class Receipt(BaseModel):
    uuid: str
    name: str