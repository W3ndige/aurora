from fastapi import FastAPI

from aurora.api import sample
from aurora.api import string
from aurora.api import relation

app = FastAPI()

app.include_router(sample.router)
app.include_router(string.router)
app.include_router(relation.router)