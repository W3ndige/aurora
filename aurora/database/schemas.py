from pydantic import BaseModel
from typing import List, Optional


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
    minhash_type: str


class Minhash(BaseModel):
    id: int
    sample_id: int
    seed: int
    hash_values: List[int]
    minhash_type: str
    sample: Sample

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class InputRelation(BaseModel):
    parent_sha256: str
    child_sha256: str
    type: str


class Relation(BaseModel):
    id: int
    parent_id: int
    child_id: int
    type: str
    strength: int
    occurance_count: int
    trait: Optional[str]
