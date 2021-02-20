from typing import List, Optional
from fastapi import APIRouter, Depends

from aurora.database import get_db, queries, schemas, models

router = APIRouter(
    prefix="/relation",
    tags=["relation"],
)


@router.get("/", response_model=List[schemas.Relation])
def get_relations(
        parent_sha256: Optional[str] = None,
        child_sha256: Optional[str] = None,
        confidence: Optional[models.RelationConfidence] = None,
        relation_type: Optional[models.RelationType] = None,
        db=Depends(get_db)
):
    parent = None
    child = None
    if parent_sha256:
        parent = queries.sample.get_sample_by_sha256(db, parent_sha256)

    if child_sha256:
        child = queries.sample.get_sample_by_sha256(db, child_sha256)

    relations = queries.relation.get_relations(db, parent, child, relation_type, confidence)
    return relations


@router.post("/", response_model=schemas.Relation)
def add_relation(relation_input: schemas.InputRelation, db=Depends(get_db)):
    parent = queries.sample.get_sample_by_sha256(db, relation_input.parent_sha256)
    child = queries.sample.get_sample_by_sha256(db, relation_input.child_sha256)

    relation = queries.relation.add_relation(
        db, parent, child, relation_input.type, relation_input.confidence
    )
    db.commit()

    return relation


@router.get("/{sha256}", response_model=List[schemas.Relation])
def get_sample_relations(
        sha256: str,
        confidence: Optional[models.RelationConfidence] = None,
        relation_type: Optional[models.RelationType] = None,
        db=Depends(get_db)
):
    sample = queries.sample.get_sample_by_sha256(db, sha256)

    return queries.relation.get_sample_relations(db, sample, relation_type, confidence)