from typing import List
from fastapi import APIRouter, Depends

from aurora.database import get_db, queries, schemas

router = APIRouter(
    prefix="/minhash",
    tags=["minhash"],
)


@router.get("/", response_model=List[schemas.Minhash])
def get_minhashes(db=Depends(get_db)):
    return queries.minhash.get_minhashes(db)
