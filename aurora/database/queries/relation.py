import logging

from typing import List, Optional
from sqlalchemy import func, tuple_, or_
from sqlalchemy.orm import Session

from aurora.database import models, schemas

logger = logging.getLogger(__name__)


def get_relations(
    db: Session,
    filters: Optional[schemas.RelationFilter] = None,
    offset: int = 0,
    limit: int = 50,
) -> List[models.Relation]:

    """Queries Relation objects from the database.

    Returns a list of relations between samples.

    Args:
        db (Session): Database session.
        filters (Optional[schemas.RelationFilter]): Optional filters used in query.
        offset (int): Offset from which the query starts.
        limit (int): Max number of relations returned in a single query.

    Returns:
        List(Relation) List of relations in a database.

    """

    query_filters = []
    if filters:
        if filters.relation_type:
            query_filters.append(models.Relation.relation_type == filters.relation_type)
        if filters.confidence:
            query_filters.append(models.Relation.confidence >= filters.confidence)

    relations = (
        db.query(models.Relation)
        .filter(*query_filters)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return relations


def get_confident_relation(db: Session) -> List[models.Relation]:
    relations_with_bigger_count = (
        db.query(models.Relation.parent_id, models.Relation.child_id)
        .group_by(models.Relation.parent_id, models.Relation.child_id)
        .having(func.count(models.Relation.parent_id) >= 2)
        .subquery()
    )

    confident_relations = (
        db.query(models.Relation)
        .filter(
            tuple_(models.Relation.parent_id, models.Relation.child_id).in_(
                relations_with_bigger_count
            )
        )
        .all()
    )

    return confident_relations


def get_relations_by_parent(
    db: Session, parent: models.Sample, filters: Optional[schemas.RelationFilter] = None
) -> List[models.Relation]:

    """Queries Relation objects from the database with specified parent.

    Returns a list of relations between samples where the parent sample is passed as a parameter.

    Args:
        db (Session): Database session.
        parent (Sample): Sample used to filter relations with specified parent.
        filters (Optional[schemas.RelationFilter]): Optional filters used in query.

    Returns:
        List(Relation) List of relations in a database.

    """

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
    db: Session, child: models.Sample, filters: Optional[schemas.RelationFilter] = None
) -> List[models.Relation]:

    """Queries Relation objects from the database with specified child.

    Returns a list of relations between samples where the child sample is passed as a parameter.

    Args:
        db (Session): Database session.
        parent (Sample): Sample used to filter relations with specified child.
        filters (Optional[schemas.RelationFilter]): Optional filters used in query.

    Returns:
        List(Relation) List of relations in a database.

    """

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
    db: Session, sample: models.Sample, filters: Optional[schemas.RelationFilter] = None
) -> List[models.Relation]:

    """Queries Relation objects from the database with specified hash.

    Returns a list of relations between samples where the parent or the child sample is passed as a parameter.

    Args:
        db (Session): Database session.
        sample (Sample): Sample used to filter relations with specified parent or child.
        filters (Optional[schemas.RelationFilter]): Optional filters used in query.

    Returns:
        List(Relation) List of relations in a database.

    """

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
            or_(
                models.Relation.parent_id == sample.id,
                models.Relation.child_id == sample.id
            )
        )
        .all()
    )

    return relations


def get_simplified_relations(
    db: Session, filters: schemas.RelationFilter = None
) -> List[models.Relation]:

    """Queries distinct Relation objects from the database.

    Returns a distinct list of relations between samples where.

    Args:
        db (Session): Database session.
        filters (Optional[schemas.RelationFilter]): Optional filters used in query.

    Returns:
        List(Relation) List of relations in a database.

    """

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
    confidence: float,
) -> models.Relation:

    """Add relation.

    Add new relation to the database.

    Args:
        db (Session): Database session.
       parent (Sample): Parent sample of the relation.
       child (Sample): Child sample of the relation.
       rel_type (str): Relation type.
       confidence (float): Float value describing confidence in relationship.
                           Value is mostly the same as similarity coefficient.

    Returns:
        Relation Newly added relation.

    """

    relation = models.Relation(
        parent=parent, child=child, relation_type=rel_type, confidence=confidence  # type: ignore
    )

    db.add(relation)

    return relation
