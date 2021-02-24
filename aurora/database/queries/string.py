from fastapi import UploadFile
from typing import List, Optional
from sqlalchemy.orm import Session

from aurora.database import models


def get_strings(db: Session):
    strings = db.query(models.String).all()
    return strings


def add_string(db: Session, value: str) -> models.String:
    string = models.String(value=value)

    db.add(string)

    return string
