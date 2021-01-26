from pydantic import BaseModel
from typing import List


class BaseFeature(BaseModel):
    data: List
    type: str

    class Config:
        orm_mode = True


class BaseSample(BaseModel):
    filename: str
    filesize: int
    filetype: str
    md5: str
    sha1: str
    sha256: str
    sha512: str

    class Config:
        orm_mode = True


class Sample(BaseSample):
    features = List[BaseFeature]

    class Config:
        arbitrary_types_allowed = True


class SampleFeature(BaseModel):
    feature: BaseFeature
    sha256: str

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
