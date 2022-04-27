from typing import Optional, Any
from schemas import Cat, CatSearchResults, CatCreate
from pathlib import Path
from fastapi import FastAPI, APIRouter, Query, HTTPException, Request
from fastapi.templating import Jinja2Templates

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH/"templates"))

app = FastAPI(title='Cats API', openapi_url='/openapi.json')
api_router = APIRouter()

CATS = [
    {
        "id": 1,
        "age": 0.5,
        "name": "Grisha",
        "color": "red",
        "description": "clever red gentleman",
        "status": "inhouse"
    }
]


@api_router.get(path='/', status_code=200, name='home')
def root(request: Request) -> dict:
    """
    ROOT get
    """
    return TEMPLATES.TemplateResponse(
        "index.html",{"request":request,"cats": CATS}
    )


@api_router.get(path='/cat/{id}', status_code=200, name='Cat', response_model=Cat)
def get_cat_by_id(*, id: int) -> dict:
    """
    Get information about single cat by cat id
    """
    result = [cat for cat in CATS if cat["id"] == id]
    if not result:
        raise HTTPException(status_code=404, detail=f'Cat with id {id} not found')

    return result[0]


@api_router.post("/cat/", status_code=201, response_model=Cat)
def create_cat(*, cat_in: CatCreate) -> dict:
    """
    Create a new cat
    """
    new_entry_id = len(CATS) + 1
    cat_entry = Cat(id=new_entry_id,age=cat_in.age, color=cat_in.color, description=cat_in.description,name=cat_in.name,status=cat_in.status)
    CATS.append(cat_entry.dict())

    return cat_entry


@api_router.get("/search/", status_code=200, name="Search", response_model=CatSearchResults)
def search_cats(keyword: Optional[str] = Query(None, min_length=3, example="red"), max_results: Optional[int] = 10) -> dict:
    """
    Search cat by words from description
    """
    if not keyword:
        return {"results": CATS[:max_results]}

    results = filter(lambda cat: keyword.lower() in cat["description"].lower(), CATS)
    return {"results": list(results)[:max_results]}


app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8090, log_level="debug")
