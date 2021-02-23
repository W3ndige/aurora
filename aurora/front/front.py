from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request, Depends
from starlette.templating import Jinja2Templates

from aurora.database import get_db, queries

templates = Jinja2Templates(directory="aurora/front/templates/")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index(request: Request, offset: int = 0, db=Depends(get_db)):
    samples = queries.sample.get_samples(db, offset=offset)

    return templates.TemplateResponse("index.html", {"request": request, "samples": samples, "offset": offset})
