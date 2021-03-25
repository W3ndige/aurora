import logging

from typing import List
from sqlalchemy import func, tuple_
from sqlalchemy.orm import Session

from aurora.database import models, schemas

logger = logging.getLogger(__name__)

def get_relations(
    db: Session, filters: schemas.RelationFilter = None
) -> List[models.Relation]:

    query_filters = []
    if filters:
        if filters.relation_type:
            query_filters.append(models.Relation.relation_type == filters.relation_type)
        if filters.confidence:
            query_filters.append(models.Relation.confidence >= filters.confidence)

    relations = db.query(models.Relation).filter(*query_filters).all()
    return relations


def get_confident_relation(db: Session) -> List[models.Relation]:
    relations_with_bigger_count = (
        db.query(models.Relation.parent_id, models.Relation.child_id)
        .group_by(
            models.Relation.parent_id,
            models.Relation.child_id
        )
        .having(func.count(models.Relation.parent_id) >= 2)
        .subquery()
    )

    confident_relations = (
        db.query(models.Relation).
        filter(
            tuple_(models.Relation.parent_id, models.Relation.child_id).
                in_(relations_with_bigger_count)
        ).all()
    )

    return confident_relations


def get_relations_by_parent(
    db: Session, parent: models.Sample, filters: schemas.RelationFilter = None
) -> List[models.Relation]:

    query_filters = []
    if filters:
        if filters.relation_type:
            query_filters.append(models.Relation.relation_type == filters.relation_type)
        if filters.confidence:
            query_filters.append(models.Relation.confidence >= filters.confidence)

    query_filters.append(models.Relation.parent_id == parent.id)

    relations = db.query(models.Relation).filter(*query_filters).all()
    return relations


def get_relations_by_child(
    db: Session, child: models.Sample, filters: schemas.RelationFilter = None
) -> List[models.Relation]:

    query_filters = []
    if filters:
        if filters.relation_type:
            query_filters.append(models.Relation.relation_type == filters.relation_type)
        if filters.confidence:
            query_filters.append(models.Relation.confidence >= filters.confidence)

    query_filters.append(models.Relation.child_id == child.id)

    relations = db.query(models.Relation).filter(*query_filters).all()
    return relations


def get_relations_by_hash(
    db: Session, sample: models.Sample, filters: schemas.RelationFilter = None
) -> List[models.Relation]:

    query_filters = []
    if filters:
        if filters.relation_type:
            query_filters.append(models.Relation.relation_type == filters.relation_type)
        if filters.confidence:
            query_filters.append(models.Relation.confidence >= filters.confidence)

    relations = (
        db.query(models.Relation)
        .filter(*query_filters)
        .filter(
            (models.Relation.parent_id == sample.id)
            | (models.Relation.child_id == sample.id)
        )
        .all()
    )

    return relations


def get_samples_with_relation(
        db: Session, filters: schemas.RelationFilter = None
) -> List[models.Relation]:

    query_filters = []
    if filters:
        if filters.relation_type:
            query_filters.append(models.Relation.relation_type == filters.relation_type)
        if filters.confidence:
            query_filters.append(models.Relation.confidence >= filters.confidence)



def get_simplified_relations(
        db: Session, filters: schemas.RelationFilter = None
) -> List[models.Relation]:

    query_filters = []
    if filters:
        if filters.relation_type:
            query_filters.append(models.Relation.relation_type == filters.relation_type)
        if filters.confidence:
            query_filters.append(models.Relation.confidence >= filters.confidence)

    relations = (
        db.query(models.Relation)
        .distinct(models.Relation.parent_id, models.Relation.child_id)
        .filter(*query_filters)
        .all()
    )

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

    db.add(relation)

    return relation
