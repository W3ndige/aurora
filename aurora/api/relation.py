from typing import List
from fastapi import APIRouter, Depends

from aurora.database import get_db, queries, schemas

router = APIRouter(
    prefix="/relation",
    tags=["relation"],
)


@router.get("/", response_model=List[schemas.Relation])
def get_all_relations(db=Depends(get_db)):
    relations = queries.relation.get_all_relations(db)
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
