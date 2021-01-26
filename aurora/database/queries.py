from typing import List
from fastapi import UploadFile
from sqlalchemy.orm import Session

from aurora.database import models
from aurora.core.utils import get_sha256


def get_samples(db: Session) -> List[models.Sample]:
    return db.query(models.Sample).all()


def get_sample(db: Session, sha256: str) -> models.Sample:
    return db.query(models.Sample) \
        .filter(models.Sample.sha256 == sha256) \
        .first()


def add_sample(db: Session, file: UploadFile) -> models.Sample:
    sha256 = get_sha256(file.file)
    sample = get_sample(db, sha256)

    if not sample:
        sample = models.Sample.from_uploadfile(file)

        db.add(sample)
        db.commit()
        db.refresh(sample)

    return sample
