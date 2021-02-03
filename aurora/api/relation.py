from fastapi import APIRouter, Depends

from aurora.database import get_db, queries, schemas

router = APIRouter(
    prefix="/relation",
    tags=["relation"],
)


@router.post("/")
def add_relation(relation_input: schemas.InputRelation, db=Depends(get_db)):
    parent = queries.sample.get_sample_by_sha256(db, relation_input.parent_sha256)
    child = queries.sample.get_sample_by_sha256(db, relation_input.child_sha256)

    queries.relation.relate_samples(db, parent, child)

    return
