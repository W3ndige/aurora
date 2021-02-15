from typing import Optional, List
from sqlalchemy.orm import Session

from aurora.database import models


def get_all_relations(db: Session) -> List[models.Relation]:
    relations = db.query(models.Relation).all()
    return relations


def add_relation(
    db: Session,
    parent: models.Sample,
    child: models.Sample,
    rel_type: str,
    confidence: str,
) -> models.Relation:

    relation = models.Relation(
        parent=parent, child=child, relation_type=rel_type, confidence=confidence
    )

    return relation


def get_relations(
    db: Session,
    parent: models.Sample,
    child: models.Sample,
    rel_type: Optional[str] = None,
    confidence: Optional[str] = None,
) -> List[models.Relation]:

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
