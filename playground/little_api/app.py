from typing import Optional, Any
from schemas.cat import CatBase, CatSearchResults, CatCreate
from db.cat_data import CATS
from pathlib import Path
from sqlalchemy.orm import Session

from fastapi import FastAPI, APIRouter, Query, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates

from schemas.cat import CatSearchResults,Cat,CatCreate
import deps
import crud

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

app = FastAPI(title='Cats API', openapi_url='/openapi.json')
api_router = APIRouter()


@api_router.get(path='/', status_code=200, name='home')
def root(
        request: Request,
        db: Session = Depends(deps.get_db),
) -> dict:
    """
    ROOT get
    """
    cats = crud.cat.get_multi(db=db, limit=10)
    return TEMPLATES.TemplateResponse(
        "index.html", {"request": request, "cats": cats}
    )


@api_router.get(path='/cat/{cat_id}', status_code=200, name='Cat', response_model=Cat)
def get_cat_by_id(
        *,
        cat_id: int,
        db: Session = Depends(deps.get_db),) -> Any:
    """
    Get information about single cat by cat_id
    """
    result = crud.cat.get(db=db,id=cat_id)
    if not result:
        raise HTTPException(status_code=404, detail=f'Cat with id {cat_id} not found')

    return result


@api_router.post("/cat/", status_code=201, response_model=Cat)
def create_cat(*, cat_in: CatCreate,
               db: Session = Depends(deps.get_db),) -> dict:
    """
    Create a new cat in database
    """
    cat_entry = crud.cat.create(db=db,obj_in=cat_in)

    return cat_entry


@api_router.get("/search/", status_code=200, name="Search", response_model=CatSearchResults)
def search_cats(keyword: Optional[str] = Query(None, min_length=3, example="red"),
                max_results: Optional[int] = 10,
                db: Session = Depends(deps.get_db),) -> dict:
    """
    Search cat by words from description
    """
    cats_list = crud.cat.get_multi(db=db,limit=max_results)
    if not keyword:
        return {"results": cats_list}

    results = filter(lambda one_cat: keyword.lower() in one_cat.description.lower(), cats_list)
    return {"results": list(results)[:max_results]}


app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8090, log_level="debug")
