from typing import Optional
from pydantic import BaseModel
from pydantic.typing import Literal


class Sample(BaseModel):
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
    encoding: Literal["ASCII", "WIDE"]
    value: str
    sha256: Optional[str]


class String(BaseModel):
    encoding: str
    value: str
    status: str
    sha256: str

    class Config:
        orm_mode = True
