from typing import List
from fastapi import APIRouter, Depends

from aurora.database import get_db, queries, schemas, models

router = APIRouter(
    prefix="/minhash",
    tags=["minhash"],
)


@router.get("/", response_model=List[schemas.Minhash])
def get_minhashes(minhash_type: models.MinhashType = None, db=Depends(get_db)):
    return queries.minhash.get_minhashes(db, minhash_type)


@router.get("/types", response_model=List[str])
def get_minhash_types():
    return list(models.MinhashType)
