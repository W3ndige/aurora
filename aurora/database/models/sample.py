from __future__ import annotations

from typing import List
from fastapi import UploadFile
from collections import namedtuple
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy

from aurora.core import utils
from aurora.database import Base
from aurora.database.models.relation import Relation

RelationInput = namedtuple("RelationInput", ["parent", "child", "type", "confidence"])


class Sample(Base):
    __tablename__ = "sample"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    filesize = Column(Integer, nullable=False)
    filetype = Column(String, nullable=False)
    md5 = Column(String(32), nullable=False, index=True)
    sha1 = Column(String(40), nullable=False, index=True)
    sha256 = Column(String(64), nullable=False, index=True, unique=True)
    sha512 = Column(String(128), nullable=False, index=True)

    minhashes = relationship("Minhash")
    ssdeep = relationship("SsDeep", uselist=False)

    children = association_proxy(
        "related_children",
        "child",
        creator=lambda relation_input: Relation(
            parent=relation_input.parent,
            child=relation_input.child,
            relation_type=relation_input.type,
            confidence=relation_input.confidence,
        ),
    )

    parents = association_proxy(
        "related_parents",
        "parent",
        creator=lambda relation_input: Relation(
            parent=relation_input.parent,
            child=relation_input.child,
            relation_type=relation_input.type,
            confidence=relation_input.confidence,
        ),
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

    def add_child(self, child: Sample, analysis_type: str, confidence: str) -> None:
        relation_input = RelationInput(
            parent=self, child=child, type=analysis_type, confidence=confidence
        )

        self.children.append(relation_input)
