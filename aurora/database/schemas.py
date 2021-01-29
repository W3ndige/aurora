from pydantic import BaseModel


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


class InputString(BaseModel):
    encoding: str
    value: str


class BaseString(BaseModel):
    encoding: str
    value: str
    status: str

    class Config:
        orm_mode = True
