from typing import List
from sqlalchemy.orm import Session

from aurora.database import models


def get_minhashes(
    db: Session, minhash_type: models.MinhashType
) -> List[models.Minhash]:
    filters = []
    if minhash_type:
        filters.append(models.Minhash.minhash_type == minhash_type)

    return db.query(models.Minhash).filter(*filters).all()


def add_minhash(
    db: Session, seed: int, hash_values: List[int], minhash_type: str
) -> models.Minhash:
    minhash_model = models.Minhash(
        seed=seed, hash_values=hash_values, minhash_type=minhash_type
    )

    db.add(minhash_model)

    return minhash_model
