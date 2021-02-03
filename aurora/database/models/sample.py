from __future__ import annotations

from fastapi import UploadFile
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy

from aurora.core import utils
from aurora.database import Base
from aurora.database.models.relation import Relation
from aurora.database.models.string import sample_string_association


class Sample(Base):
    __tablename__ = "sample"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False, index=True)
    filesize = Column(Integer, nullable=False, index=True)
    filetype = Column(String, nullable=False, index=True)
    md5 = Column(String(32), nullable=False, index=True, unique=True)
    sha1 = Column(String(40), nullable=False, index=True, unique=True)
    sha256 = Column(String(64), nullable=False, index=True, unique=True)
    sha512 = Column(String(128), nullable=False, index=True, unique=True)

    strings = relationship(
        "String", secondary=sample_string_association, back_populates="samples"
    )

    parents = association_proxy(
        "parent_samples",
        "parent",
        creator=lambda samples: Relation(parent=samples[0], child=samples[1])
    )

    children = association_proxy(
        "children_samples",
        "child",
        creator=lambda samples: Relation(parent=samples[0], child=samples[1])
    )

    @staticmethod
    def from_uploadfile(file: UploadFile) -> Sample:
        file.file.seek(0, 2)

        filename = file.filename
        filesize = file.file.tell()
        filetype = utils.get_magic(file.file)
        md5 = utils.get_md5(file.file)
        sha1 = utils.get_sha1(file.file)
        sha256 = utils.get_sha256(file.file)
        sha512 = utils.get_sha512(file.file)

        sample = Sample(
            filename=filename,
            filesize=filesize,
            filetype=filetype,
            md5=md5,
            sha1=sha1,
            sha256=sha256,
            sha512=sha512,
        )

        return sample

    def add_child_sample(self, sample: Sample) -> None:
        self.children.append((self, sample))
