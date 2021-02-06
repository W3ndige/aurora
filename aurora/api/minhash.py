from fastapi import APIRouter, Depends

from aurora.database import get_db, queries

router = APIRouter(
    prefix="/minhash",
    tags=["minhash"],
)


@router.get("/")
def get_minhashes(db=Depends(get_db)):
    return queries.minhash.get_minhashes(db)
