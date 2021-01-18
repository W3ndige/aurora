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


@router.post("/")
def upload_sample(file: UploadFile = File(...), db=Depends(get_db)):
    sample = queries.add_sample(db, file)

    try:
        karton.push_file(file, sample.sha256)
    except RuntimeError:
        pass

    return sample


@router.get("/{sha256}")
def get_sample(sha256: str, db=Depends(get_db)):
    sample = queries.get_sample(db, sha256)

    return sample


@router.get("/{sha256}/feature")
def get_sample_features(sha256: str, db=Depends(get_db)):
    sample = queries.get_sample(db, sha256)

    return sample.features


@router.post("/{sha256}/feature")
def upload_sample_feature(sha256: str, feature: schemas.Feature,
                          db=Depends(get_db)):

    feature = queries.add_sample_feature(
        db,
        sha256,
        feature
    )

    return feature
