from fastapi import FastAPI

from aurora.api import sample
from aurora.api import feature

app = FastAPI()

app.include_router(sample.router)
app.include_router(feature.router)
