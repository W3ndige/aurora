from sqlalchemy.orm import Session

from aurora.database import models


def get_relation(
    db: Session, parent: models.Sample, child: models.Sample, type: str
) -> models.Relation:

    relation = (
        db.query(models.Relation)
        .filter(models.Relation.parent_id == parent.id)
        .filter(models.Relation.child_id == child.id)
        .filter(models.Relation.type == type)
        .first()
    )

    return relation


def add_relation(
    db: Session, parent: models.Sample, child: models.Sample, rel_type: str
) -> models.Relation:

    relation = get_relation(db, parent, child, rel_type)
    if relation:
        update_occurance_count(db, relation)
        return relation

    parent.add_child_sample(child, rel_type)
    db.commit()

    relation = get_relation(db, parent, child, rel_type)

    return relation


def update_occurance_count(db: Session, relation: models.Relation) -> models.Relation:
    relation.occurance_count += 1
    db.commit()

    return relation
