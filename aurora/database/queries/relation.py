from sqlalchemy.orm import Session

from aurora.database import models


def add_relation(
    db: Session, parent: models.Sample, child: models.Sample, rel_type: str, confidence: str
) -> models.Relation:

    relation = parent.add_child(child, rel_type, confidence)
    db.commit()

    return relation
