from fastapi import UploadFile
from sqlalchemy.orm import Session

from aurora.database import models, schemas
from aurora.core.utils import get_sha256


def get_sample(db: Session, sha256: str) -> models.Sample:
    return db.query(models.Sample) \
           .filter(models.Sample.sha256 == sha256).first()


def add_sample(db: Session, file: UploadFile) -> models.Sample:
    sha256 = get_sha256(file.file)
    sample = get_sample(db, sha256)

    if not sample:
        sample = models.Sample.from_uploadfile(file)

        db.add(sample)
        db.commit()
        db.refresh(sample)

    return sample


def add_sample_feature(db: Session, sha256: str,
                       feature_scheme: schemas.feature) -> models.Feature:

    sample = get_sample(db, sha256)

    if not sample:
        return None

    feature = models.Feature.from_list(
        feature_scheme.data,
        feature_scheme.type
    )

    sample.features.append(feature)
    db.commit()

    return feature
