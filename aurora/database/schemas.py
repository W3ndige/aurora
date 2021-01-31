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
    sha256: Optional[str]


class String(BaseModel):
    id: int
    value: str
    type: str
    sha256: str

    class Config:
        orm_mode = True
