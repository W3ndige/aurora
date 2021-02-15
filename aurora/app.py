from fastapi import FastAPI

from aurora.api import sample
from aurora.api import minhash
from aurora.api import relation
from aurora.api import ssdeep

app = FastAPI()

app.include_router(sample.router)
app.include_router(minhash.router)
app.include_router(relation.router)
app.include_router(ssdeep.router)
