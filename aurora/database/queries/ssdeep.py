from fastapi import UploadFile
from typing import List, Optional
from sqlalchemy.orm import Session

from aurora.database import models


def get_ssdeep_hashes(
    db: Session, chunksize: Optional[int] = None
) -> List[models.SsDeep]:

    """Queries Ssdeep objects from the database.

    Returns a list of ssdeep hashes.

    Args:
        db (Session): Database session.
        chunksize (int): Optional chunksize to filter hashes.

    Returns:
        List(SsDeep) List of ssdeep hashes in a database.

    """

    filters = []
    if chunksize:
        filters.append(models.SsDeep.chunksize == chunksize)

    hashes = db.query(models.SsDeep).filter(*filters).all()

    return hashes


def add_ssdeep(db: Session, file: UploadFile) -> models.SsDeep:

    """Add ssdeep.

    Add new ssdeep hash to the database.

    Args:
       db (Session): Database session.
       file (UploadFile): Sample file from which ssdeep will be calculated.

    Returns:
        SsDeep Newly added ssdeep hash.

    """

    ssdeep = models.SsDeep.from_uploadfile(file)

    db.add(ssdeep)

    return ssdeep
