from fastapi import UploadFile
from typing import List, Optional
from sqlalchemy.orm import Session

from aurora.database import models, schemas
from aurora.core.utils import get_sha256


def get_samples(db: Session) -> List[models.Sample]:
    return db.query(models.Sample).all()


def get_sample(db: Session, sha256: str) -> models.Sample:
    return db.query(models.Sample) \
        .filter(models.Sample.sha256 == sha256) \
        .first()


def get_strings(db: Session) -> List[models.String]:
    return db.query(models.String).all()


def add_sample(db: Session, file: UploadFile) -> models.Sample:
    sha256 = get_sha256(file.file)
    sample = get_sample(db, sha256)

    if not sample:
        sample = models.Sample.from_uploadfile(file)

        db.add(sample)
        db.commit()
        db.refresh(sample)

    return sample


def add_string(db: Session, data: schemas.BaseString) -> models.String:
    string = get_exact_string(db, data)

    if not string:
        string = models.String(
            type=data.type,
            value=data.value,
            status="new"
        )

        db.add(string)
        db.commit()
        db.refresh(string)
    else:
        # Hardcoded value, will be derived from the number of total samples
        if get_num_of_string_samples(db, string.id) > 10:
            update_string_status(db, string.id, "common")

    return string


def add_sample_string(db: Session, sha256: str,
                      str_data: schemas.BaseString) -> models.String:

    sample = get_sample(db, sha256)
    string = add_string(db, str_data)

    sample.strings.append(string)

    db.commit()

    return string


def update_string_status(db: Session, id: int, status: str) -> models.String:
    string = db.query(models.String) \
        .filter(models.String.id == id) \
        .first()

    string.status = status

    db.commit()

    return string


def get_exact_string(db: Session, data: schemas.BaseString) \
        -> Optional[models.String]:

    string = db.query(models.String) \
        .filter(models.String.type == data.type) \
        .filter(models.String.value == data.value) \
        .first()

    return string or None


def get_sample_strings(db: Session, sha256: str) -> List:
    sample = get_sample(db, sha256)

    if not sample:
        return None

    return sample.strings


def get_num_of_string_samples(db: Session, id: int) -> int:

    string = db.query(models.String) \
        .filter(models.String.id == id) \
        .first()

    num_of_samples = len(string.samples)

    return num_of_samples
