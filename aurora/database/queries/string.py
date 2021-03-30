from fastapi import UploadFile
from typing import List, Optional
from sqlalchemy.orm import Session

from aurora.database import models


def get_strings(db: Session, offset: int = 0, limit: int = 50):
    strings = db.query(models.String).offset(offset).limit(limit).all()
    return strings


def get_unique_strings(db: Session, offset: int = 0, limit: int = 50):
    strings = db.query(models.String).distinct(models.String.sha256).offset(offset).limit(limit).all()
    return strings


def add_string(db: Session, value: str, sha256: str, heuristic: str) -> models.String:
    string = models.String(value=value, sha256=sha256, heuristic=heuristic)

    db.add(string)

    return string


def get_string(db: Session, sha256: str) -> models.String:
    string = db.query(models.String).filter(models.String.sha256 == sha256).first()

    return string