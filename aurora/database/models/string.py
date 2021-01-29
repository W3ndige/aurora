from __future__ import annotations

import hashlib
import sqlalchemy as sql

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM

from aurora.database import Base

Encoding = ENUM("ASCII", "WIDE", name="encoding")
Status = ENUM("NEW", "COMMON", "SUSPICIOUS", name="status")

sample_string_association = sql.Table(
    "sample_string_association",
    Base.metadata,
    sql.Column("sample_id", sql.Integer, sql.ForeignKey("sample.id")),
    sql.Column("string_id", sql.Integer, sql.ForeignKey("string.id")),
)


class String(Base):
    __tablename__ = "string"

    id = sql.Column(sql.Integer, primary_key=True)
    encoding = sql.Column(Encoding, nullable=False)
    value = sql.Column(sql.String, nullable=False)
    sha256 = sql.Column(sql.String(128), nullable=False)
    status = sql.Column(Status, nullable=False)

    unique_encoded_string = sql.UniqueConstraint("encoding", "sha256")

    samples = relationship(
        "Sample", secondary=sample_string_association, back_populates="strings"
    )

    def __init__(self, encoding: str, value: str, status, sha256: str = None):
        if not sha256:
            sha256 = hashlib.sha256(value.encode("utf-8")).hexdigest()

        self.encoding = encoding
        self.value = value
        self.sha256 = sha256
        self.status = status
