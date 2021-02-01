from typing import List
from fastapi import APIRouter, UploadFile, File, Depends

from aurora.core import karton
from aurora.database import get_db, queries, schemas

router = APIRouter(
    prefix="/sample",
    tags=["sample"],
)


@router.get("/")
def get_samples(db=Depends(get_db)):
    return queries.sample.get_samples(db)


@router.post("/", response_model=schemas.Sample)
def add_sample(file: UploadFile = File(...), db=Depends(get_db)):
    sample = queries.sample.add_sample(db, file)

    try:
        karton.push_file(file, sample.sha256)
    except RuntimeError:
        pass

    return sample


@router.get("/{sha256}", response_model=schemas.Sample)
def get_sample(sha256: str, db=Depends(get_db)):
    sample = queries.sample.get_sample(db, sha256)

    return sample


@router.post("/{sha256}/string", response_model=schemas.String)
def add_string(sha256: str, string: schemas.InputString, db=Depends(get_db)):
    sample = queries.sample.get_sample_by_sha256(db, sha256)
    submitted_string = queries.string.add_string(
        db, string.value, string.trait
    )

    queries.string.add_string_to_sample(
        db,
        sample,
        submitted_string
    )

    return submitted_string


@router.get("/{sha256}/strings", response_model=List[schemas.String])
def get_strings(sha256: str, db=Depends(get_db)):
    strings = queries.string.get_sample_strings(db, sha256)

    return strings
