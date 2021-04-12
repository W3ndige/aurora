from __future__ import annotations

import sqlalchemy as sql

from fastapi import UploadFile
from collections import namedtuple
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.ext.associationproxy import association_proxy

from aurora.core import utils
from aurora.database import Base
from aurora.database.models.relation import Relation

RelationInput = namedtuple("RelationInput", ["parent", "child", "type", "confidence"])

if TYPE_CHECKING:
    from aurora.database.models import Minhash  # noqa: F401
    from aurora.database.models import String  # noqa: F401
    from aurora.database.models import SsDeep  # noqa: F401


class Sample(Base):
    __tablename__ = "sample"

    id = sql.Column(sql.Integer, primary_key=True)
    filename = sql.Column(sql.String, nullable=False)
    filesize = sql.Column(sql.Integer, nullable=False)
    filetype = sql.Column(sql.String, nullable=False)
    md5 = sql.Column(sql.String(32), nullable=False, index=True)
    sha1 = sql.Column(sql.String(40), nullable=False, index=True)
    sha256 = sql.Column(sql.String(64), nullable=False, index=True, unique=True)
    sha512 = sql.Column(sql.String(128), nullable=False, index=True)

    minhashes: RelationshipProperty[List[Minhash]] = relationship("Minhash")
    strings: RelationshipProperty[List[String]] = relationship("String")
    ssdeep = relationship("SsDeep", uselist=False)

    children = association_proxy(
        "related_children",
        "child",
        creator=lambda relation_input: Relation(
            parent=relation_input.parent,  # type: ignore
            child=relation_input.child,  # type: ignore
            relation_type=relation_input.type,  # type: ignore
            confidence=relation_input.confidence,  # type: ignore
        ),
    )

    parents = association_proxy(
        "related_parents",
        "parent",
        creator=lambda relation_input: Relation(
            parent=relation_input.parent,  # type: ignore
            child=relation_input.child,  # type: ignore
            relation_type=relation_input.type,  # type: ignore
            confidence=relation_input.confidence,  # type: ignore
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
