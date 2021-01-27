from fastapi import FastAPI

from aurora.api import sample
from aurora.api import string

app = FastAPI()

app.include_router(sample.router)
app.include_router(string.router)
