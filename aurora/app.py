from fastapi import FastAPI

from aurora.api import sample

app = FastAPI()

app.include_router(sample.router)
