import ssdeep

from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import UploadFile
from typing import List, Optional
from logging import getLogger

from aurora.database import models

logger = getLogger(__name__)


def get_samples(db: Session, offset: int = 0, limit: int = 50) -> List[models.Sample]:

    """Queries Sample objects from the database.

    Returns a list of samples.

    Args:
        db (Session): Database session.
        offset (int): Offset from which the query starts.
        limit (int): Max number of relations returned in a single query.

    Returns:
        List(Relation) List of relations in a database.

    """

    return db.query(models.Sample).offset(offset).limit(limit).all()


def get_number_of_samples(db: Session) -> int:

    """Returns a total number of samples.

    Args:
        db (Session): Database session.

    Returns:
        int Total number of samples in database.

    """

    return db.query(models.Sample).count()


def get_sample_by_md5(db: Session, md5: str) -> Optional[models.Sample]:

    """Returns a sample by the MD5 hash.

    Queries a sample which MD5 hash is equal to the passed one.

    Args:
         db (Session): Database session.
         sha256 (str): MD5 hash of the sample.

    Returns:
        Sample Sample with the specified hash.

    """

    return db.query(models.Sample).filter(models.Sample.md5 == md5).first()


def get_sample_by_sha1(db: Session, sha1: str) -> Optional[models.Sample]:

    """Returns a sample by the SHA1 hash.

    Queries a sample which SHA1 hash is equal to the passed one.

    Args:
         db (Session): Database session.
         sha256 (str): SHA1 hash of the sample.

    Returns:
        Sample Sample with the specified hash.

    """

    return db.query(models.Sample).filter(models.Sample.sha1 == sha1).first()


def get_sample_by_sha256(db: Session, sha256: str) -> Optional[models.Sample]:

    """Returns a sample by the SHA256 hash.

    Queries a sample which SHA256 hash is equal to the passed one.

    Args:
         db (Session): Database session.
         sha256 (str): SHA256 hash of the sample.

    Returns:
        Sample Sample with the specified hash.

    """

    return db.query(models.Sample).filter(models.Sample.sha256 == sha256).first()


def get_sample_by_sha512(db: Session, sha512: str) -> Optional[models.Sample]:

    """Returns a sample by the SHA512 hash.

    Queries a sample which SHA512 hash is equal to the passed one.

    Args:
         db (Session): Database session.
         sha256 (str): SHA512 hash of the sample.

    Returns:
        Sample Sample with the specified hash.

    """

    return db.query(models.Sample).filter(models.Sample.sha512 == sha512).first()


def get_sample_parents(db: Session, sample: models.Sample) -> List[models.Sample]:

    """Returns parents of the sample.

    Queries samples which child is the sample specified as argument.

    Args:
         db (Session): Database session.
         sample (Sample): Sample whose parents are queried.

    Returns:
        List(Sample) List of parent samples related to the argument sample.

    """

    return (
        db.query(models.Sample)
        .distinct()
        .filter(models.Sample.children.any(models.Relation.child_id == sample.id))
        .all()
    )


def get_sample_children(db: Session, sample: models.Sample) -> List[models.Sample]:

    """Returns children of the sample.

    Queries samples which parent is the sample specified as argument.

    Args:
         db (Session): Database session.
         sample (Sample): Sample whose children are queried.

    Returns:
        List(Sample) List of child samples related to the argument sample.

    """

    return (
        db.query(models.Sample)
        .distinct()
        .filter(models.Sample.parents.any(models.Relation.parent_id == sample.id))
        .all()
    )


def get_sample_related(db: Session, sample: models.Sample) -> List[models.Sample]:

    """Returns related samples.

    Returns both parent and children samples.

    Args:
         db (Session): Database session.
         sample (Sample): Sample whose related samples are queried.

    Returns:
        List(Sample) List of related samples related to the argument sample.

    """

    return (
        db.query(models.Sample)
        .distinct()
        .filter(
            or_(
                models.Sample.parents.any(models.Relation.parent_id == sample.id),
                models.Sample.children.any(models.Relation.child_id == sample.id),
            )
        )
        .all()
    )


def get_samples_with_string(db: Session, string: models.String) -> List[models.Sample]:

    """Returns samples containing string.

    Queries samples which contain string specified as argument..

    Args:
         db (Session): Database session.
         string (String): String which queried samples have to contain..

    Returns:
        List(Sample) List of samples containing specified string.

    """

    return (
        db.query(models.Sample)
        .filter(models.Sample.strings.any(models.String.sha256 == string.sha256))
        .all()
    )


def get_samples_by_ssdeep(db: Session, ssdeep_hash: str, cutoff_value: float = 0.5) -> List[models.Sample]:

    chunksize = int(ssdeep_hash.split(":")[0])

    candidate_samples = (
        db.query(models.Sample)
        .join(models.SsDeep)
        .filter(models.SsDeep.chunksize == chunksize)
        .all()
    )

    samples = []
    for candidate in candidate_samples:
        if ssdeep.compare(candidate.ssdeep.ssdeep, ssdeep_hash) > cutoff_value:
            samples.append(candidate)

    return samples


def add_sample(db: Session, file: UploadFile) -> models.Sample:

    """Add sample.

    Add new sample to the database.

    Args:
       db (Session): Database session.
       file (UploadFile): Sample file.

    Returns:
        Sample Newly added sample.

    """

    sample = models.Sample.from_uploadfile(file)
    db.add(sample)

    return sample
