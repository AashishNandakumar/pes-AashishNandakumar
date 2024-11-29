from pydantic import BaseModel
from datetime import datetime


class ItemBase(BaseModel):
    id: int
    name: str
    description: str | None = None
    quantity: int


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    last_modified: datetime

    class Config:
        orm_mode = True
