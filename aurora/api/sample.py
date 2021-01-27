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
    return


@router.post("/", response_model=schemas.BaseSample)
def add_sample(file: UploadFile = File(...), db=Depends(get_db)):
    sample = queries.add_sample(db, file)

    try:
        karton.push_file(file, sample.sha256)
    except RuntimeError:
        pass

    return sample


@router.get("/{sha256}", response_model=schemas.BaseSample)
def get_sample(sha256: str, db=Depends(get_db)):
    sample = queries.get_sample(db, sha256)

    return sample


@router.post("/{sha256}/string", response_model=schemas.BaseString)
def add_string(sha256: str, string: schemas.BaseString, db=Depends(get_db)):
    string = queries.add_sample_string(db, sha256, string)

    return string


@router.get("/{sha256}/strings", response_model=List[schemas.BaseString])
def get_strings(sha256: str, db=Depends(get_db)):
    strings = queries.get_sample_strings(db, sha256)

    return strings
