from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from aurora.database import models


def get_minhashes(
    db: Session, minhash_type: Optional[models.MinhashType] = None
) -> List[models.Minhash]:

    """Queries Minhash objects from the database.

    Returns a list of Minhash objects from the database.

    Args:
        db (Session): Database session.
        minhash_type (Optional(MinhashType)): Optional MinhashType to filter out objects.

    Returns:
        List(Minhash) Returns a list of Minhash objects in the database.

    """

    filters = []
    if minhash_type:
        filters.append(models.Minhash.minhash_type == minhash_type)

    return db.query(models.Minhash).filter(*filters).all()


def get_sample_minhash(
    db: Session, sample: models.Sample, type: models.MinhashType
) -> models.Minhash:

    """Queries Minhash objects tat belong to the passed sample.

    Returns a list of Minhash objects whose `sample_id` is equal to the `id` of passed sample..

    Args:
        db (Session): Database session.
        sample (Sample): Sample object to which minhashes will be related.
        minhash_type (Optional(MinhashType)): Optional MinhashType to filter out objects.

    Returns:
        List(Minhash) Returns a list of Minhash objects in the database.

    """

    return (
        db.query(models.Minhash)
        .filter(models.Minhash.sample_id == sample.id)
        .filter(models.Minhash.minhash_type == type)
        .all()
    )


def add_minhash(
    db: Session,
    seed: int,
    hash_values: List[int],
    minhash_type: str,
    extra_data: Optional[Dict[str, Any]] = None,
) -> models.Minhash:
    """Creates a new Minhash object..

    Creates ands add to databse a new minhash object using the passed parameters.

    Args:
        db (Session): Database session.
        seed (int): Seed of the minhash.
        hash_values (List(int)): List of hash values of the minhash.
        minhash_type (MinhashType): Type of the minhash.
        extra_data (Optional(Dict[(str, Any))): Optional extra data stored with the minhash.

    Returns:
        Minhash Returns created minhash object..

    """

    minhash_model = models.Minhash(
        seed=seed,
        hash_values=hash_values,
        minhash_type=minhash_type,
        extra_data=extra_data,
    )

    db.add(minhash_model)

    return minhash_model
