import datasketch  # type: ignore

from typing import List
from fastapi import APIRouter, Depends

from aurora.database import get_db, queries, schemas, models

router = APIRouter(
    prefix="/minhash",
    tags=["minhash"],
)


@router.get("/", response_model=List[schemas.Minhash])
def get_minhashes(minhash_type: str = None, db=Depends(get_db)):
    return queries.minhash.get_minhashes(db, minhash_type)


@router.get("/types", response_model=List[str])
def get_minhash_types():
    return list(models.MinhashType)


@router.post("/compare", response_model=float)
def compare_minhash(m1: schemas.InputMinhash, m2: schemas.InputMinhash):
    m1_lean = datasketch.LeanMinHash(seed=m1.seed, hashvalues=m1.hash_values)
    m2_lean = datasketch.LeanMinHash(seed=m2.seed, hashvalues=m2.hash_values)

    return m1_lean.jaccard(m2_lean)
