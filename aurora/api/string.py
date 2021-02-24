from typing import List, Optional
from fastapi import APIRouter, Depends

from aurora.database import get_db, queries, schemas

router = APIRouter(
    prefix="/string",
    tags=["string"],
)


@router.get("/", response_model=List[schemas.String])
def get_strings(db=Depends(get_db)):
    return queries.string.get_strings(db)
