from typing import Optional, List
from sqlalchemy.orm import Session

from aurora.database import models


def get_relations(
        db: Session,
        parent: models.Sample = None,
        child: models.Sample = None,
        relation_type: models.RelationType = None,
        confidence: models.RelationConfidence = None
) -> List[models.Relation]:

    filters = []
    if parent:
        filters.append(models.Relation.parent_id == parent.id)

    if child:
        filters.append(models.Relation.child_id == child.id)

    if relation_type:
        filters.append(models.Relation.relation_type == relation_type)

    if confidence:
        filters.append(models.Relation.confidence == confidence)

    relations = db.query(models.Relation).filter(*filters).all()
    return relations


def get_sample_relations(
        db: Session,
        sample: models.Sample,
        relation_type: models.RelationType = None,
        confidence: models.RelationConfidence = None
) -> List[models.Relation]:

    filters = []
    if relation_type:
        filters.append(models.Relation.relation_type == relation_type)

    if confidence:
        filters.append(models.Relation.confidence == confidence)

    return (
        db.query(models.Relation)
        .filter(
            (models.Relation.child_id == sample.id) | (models.Relation.parent_id == sample.id)
        ).filter(*filters)
        .all()
    )


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