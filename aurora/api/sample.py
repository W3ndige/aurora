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


@router.get("/{sha256}/parents", response_model=List[schemas.Sample])
def get_parents(sha256: str, db=Depends(get_db)):
    sample = queries.sample.get_sample_by_sha256(db, sha256)

    if not sample:
        return None

    return queries.sample.get_sample_parents(db, sample)


@router.get("/{sha256}/children", response_model=List[schemas.Sample])
def get_children(sha256: str, db=Depends(get_db)):
    sample = queries.sample.get_sample_by_sha256(db, sha256)

    if not sample:
        return None

    return queries.sample.get_sample_children(db, sample)
