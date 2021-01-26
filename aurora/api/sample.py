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
def upload_sample(file: UploadFile = File(...), db=Depends(get_db)):
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
