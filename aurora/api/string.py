from typing import List
from fastapi import APIRouter, Depends

from aurora.database import get_db, queries, schemas

router = APIRouter(
    prefix="/string",
    tags=["string"],
)


@router.get("/", response_model=List[schemas.BaseString])
def get_samples(db=Depends(get_db)):
    return queries.get_strings(db)
