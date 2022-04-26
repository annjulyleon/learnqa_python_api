from pydantic import BaseModel
from typing import Sequence


class Cat(BaseModel):
    id: int
    age: float
    color: str
    description: str
    name: str
    status: str


class CatSearchResults(BaseModel):
    results: Sequence[Cat]


class CatCreate(BaseModel):
    age: float
    color: str
    description: str
    name: str
    status: str
    #submitted_id: int
