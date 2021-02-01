import hashlib

from typing import List, Optional
from sqlalchemy.orm import Session

from aurora.database import models
from aurora.database.queries.sample import get_number_of_samples


def get_strings(db: Session) -> List[models.String]:
    return db.query(models.String).all()


def get_string_by_id(db: Session, id: int) -> Optional[models.String]:
    string = (
        db.query(models.String)
        .filter(models.String.id == id)
        .first()
    )

    return string


def get_string_by_sha256(db: Session, sha256: str) -> Optional[models.String]:
    string = (
        db.query(models.String)
        .filter(models.String.sha256 == sha256)
        .first()
    )

    return string


def get_string_by_value(db: Session, value: str) -> Optional[models.String]:
    string = (
        db.query(models.String)
        .filter(models.String.value == value)
        .first()
    )

    return string


def get_strings_samples(
    db: Session, string: models.String
) -> List[models.Sample]:

    return string.samples


def get_strings_samples_len(db: Session, string: models.String) -> int:
    return len(string.samples)


def add_string_to_sample(
    db: Session, sample: models.Sample, string: models.String
) -> None:

    sample.strings.append(string)
    db.commit()


def add_string(
    db: Session, value: str, trait: Optional[str] = None
) -> models.String:
    sha256 = hashlib.sha256(value.encode("utf-8")).hexdigest()
    string = get_string_by_sha256(db, sha256)

    if not string:
        string = models.String(
            value=value, type="Uncategorized", trait=trait, sha256=sha256
        )

        db.add(string)
        db.commit()
        db.refresh(string)

    else:
        # TODO(W3ndige): Add value dervied from the number of samples.
        alot_coefficient = (get_number_of_samples(db) * 0.5)
        if get_strings_samples_len(db, string) > alot_coefficient:
            string = update_string_type(db, string, "Common")

    return string


def update_string_type(
    db: Session, string: models.String, type: str
) -> models.String:

    string.type = type
    db.commit()
    db.refresh(string)

    return string
