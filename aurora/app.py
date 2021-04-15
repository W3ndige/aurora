from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

from aurora.api import sample
from aurora.api import minhash
from aurora.api import relation
from aurora.api import ssdeep
from aurora.api import string

from aurora.front import front

api_v1 = APIRouter()

api_v1.include_router(sample.router)
api_v1.include_router(minhash.router)
api_v1.include_router(relation.router)
api_v1.include_router(ssdeep.router)
api_v1.include_router(string.router)

app = FastAPI()

app.mount("/static", StaticFiles(directory="aurora/front/static"), name="static")

app.include_router(api_v1, prefix="/api/v1")
app.include_router(front.router, prefix="")
