import ssdeep  # type: ignore

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException

from aurora.database import get_db, queries, schemas

router = APIRouter(
    prefix="/ssdeep",
    tags=["ssdeep"],
)


@router.get("/", response_model=List[schemas.SsDeep])
def get_ssdeep_hashes(chunksize: Optional[int] = None, db=Depends(get_db)):
    return queries.ssdeep.get_ssdeep_hashes(db, chunksize=chunksize)


@router.post("/compare", response_model=float)
def compare_ssdeep(s1: str, s2: str):
    try:
        coefficient = ssdeep.compare(s1, s2) / 100.0
    except ssdeep.InternalError:
        raise HTTPException(status_code=500, detail="SsDeep compare failed.")

    return coefficient
