from fastapi import UploadFile
from typing import List, Optional
from sqlalchemy.orm import Session

from aurora.database import models


def get_ssdeep_hashes(
    db: Session, chunksize: Optional[int] = None
) -> List[models.SsDeep]:
    filters = []
    if chunksize:
        filters.append(models.SsDeep.chunksize == chunksize)

    hashes = db.query(models.SsDeep).filter(*filters).all()

    return hashes


def add_ssdeep(db: Session, file: UploadFile) -> models.SsDeep:
    ssdeep = models.SsDeep.from_uploadfile(file)

    return ssdeep
