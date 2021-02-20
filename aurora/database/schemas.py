from pydantic import BaseModel
from typing import List

from aurora.database.models.relation import RelationType
from aurora.database.models.minhash import MinhashType


class Sample(BaseModel):
    id: int
    filename: str
    filesize: int
    filetype: str
    md5: str
    sha1: str
    sha256: str
    sha512: str

    class Config:
        orm_mode = True


class InputMinhash(BaseModel):
    seed: int
    hash_values: List[int]
    minhash_type: MinhashType


class Minhash(BaseModel):
    id: int
    seed: int
    hash_values: List[int]
    minhash_type: MinhashType
    sample: Sample

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class InputRelation(BaseModel):
    parent_sha256: str
    child_sha256: str
    type: RelationType
    confidence: str


class Relation(BaseModel):
    id: int
    parent_id: int
    child_id: int
    relation_type: RelationType
    confidence: str

    class Config:
        orm_mode = True


class SsDeep(BaseModel):
    id: int
    chunksize: int
    ssdeep: str
    sample: Sample

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
