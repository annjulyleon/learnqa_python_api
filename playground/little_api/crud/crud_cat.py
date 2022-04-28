from crud.base import CRUDBase
from models.cat import Cat
from schemas.cat import CatCreate, CatUpdate


class CRUDCat(CRUDBase[Cat,CatCreate, CatUpdate]):
    ...

cat = CRUDCat(Cat)