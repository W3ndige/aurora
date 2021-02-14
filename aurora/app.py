from fastapi import FastAPI

from aurora.api import sample
from aurora.api import minhash
from aurora.api import relation

app = FastAPI()

app.include_router(sample.router)
app.include_router(minhash.router)
app.include_router(relation.router)
