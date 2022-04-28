from pydantic import BaseModel
from typing import Sequence

"""
PYDANTIC SCHEMES
"""


class CatBase(BaseModel):
    age: float
    color: str
    description: str
    name: str
    status: str

class CatCreate(CatBase):
    age: float
    color: str
    description: str
    name: str
    status: str
    caretaker_id: str


class CatUpdate(CatBase):
    description: str


"""
DB SCHEMES
"""


# Properties shared by models stored in DB
class CatInDBBase(CatBase):
    id: int
    caretaker_id: int

    class Config:
        orm_mode = True


# Why make the distinction between a Cat and CatInDB? \
# This allows us in future to separate fields which are only relevant for the DB, \
# or which we don’t want to return to the client (such as a password field).
# Properties to return to the client
class Cat(CatInDBBase):
    pass


# Properties stored in DB
class CatInDB(CatInDBBase):
    pass


class CatSearchResults(BaseModel):
    results: Sequence[Cat]