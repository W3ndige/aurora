from typing import Optional
from pydantic import BaseModel


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


class InputString(BaseModel):
    value: str
    trait: Optional[str]
    sha256: Optional[str]


class String(BaseModel):
    id: int
    value: str
    trait: Optional[str]
    type: str
    sha256: str

    class Config:
        orm_mode = True


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
