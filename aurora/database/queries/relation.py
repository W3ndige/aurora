from typing import Optional, List
from sqlalchemy.orm import Session

from aurora.database import models


def add_relation(
    db: Session,
    parent: models.Sample,
    child: models.Sample,
    rel_type: str,
    confidence: str,
) -> None:

    parent.add_child(child, rel_type, confidence)


def get_relations(
    db: Session,
    parent: models.Sample,
    child: models.Sample,
    rel_type: Optional[str] = None,
    confidence: Optional[str] = None,
) -> List[models.Relations]:

    filters = [
        models.Relation.parent_id == parent.id,
        models.Relation.child_id == child.id,
    ]

    if rel_type:
        filters.append(models.Relation.relation_type == rel_type)

    if confidence:
        filters.append(models.Relation.confidence == confidence)

    relations = db.query(models.Relation).filter(*filters).all()

    return relations
