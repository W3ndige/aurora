from typing import List
from fastapi import APIRouter, Depends

from aurora.database import get_db, queries, schemas

router = APIRouter(
    prefix="/string",
    tags=["string"],
)


@router.get("/", response_model=List[schemas.String])
def get_strings(db=Depends(get_db)):
    return queries.string.get_strings(db)


@router.post("/", response_model=schemas.String)
def add_string(string: schemas.InputString, db=Depends(get_db)):
    string = queries.string.add_string(db, string.value)

    return string


@router.get("/{sha256}", response_model=schemas.String)
def get_string(sha256: str, db=Depends(get_db)):
    return queries.string.get_string_by_sha256(db, sha256)


@router.get("/{sha256}/samples", response_model=List[schemas.Sample])
def get_string_samples(sha256: str, db=Depends(get_db)):
    string = queries.string.get_string_by_sha256(db, sha256)

    return queries.string.get_strings_samples(db, string)
