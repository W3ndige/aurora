from typing import List, Optional
from fastapi import APIRouter, Depends

from aurora.database import get_db, queries, schemas

router = APIRouter(
    prefix="/ssdeep",
    tags=["ssdeep"],
)


@router.get("/", response_model=List[schemas.SsDeep])
def get_samples(chunksize: Optional[int] = None, db=Depends(get_db)):
    return queries.ssdeep.get_ssdeep_hashes(db, chunksize=chunksize)
