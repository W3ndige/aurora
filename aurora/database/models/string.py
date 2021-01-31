from __future__ import annotations

import hashlib
import sqlalchemy as sql

from sqlalchemy.orm import relationship

from aurora.database import Base

sample_string_association = sql.Table(
    "sample_string_association",
    Base.metadata,
    sql.Column("sample_id", sql.Integer, sql.ForeignKey("sample.id")),
    sql.Column("string_id", sql.Integer, sql.ForeignKey("string.id")),
)


class String(Base):
    __tablename__ = "string"

    id = sql.Column(sql.Integer, primary_key=True)
    value = sql.Column(sql.String, nullable=False)
    sha256 = sql.Column(sql.String(128), nullable=False, unique=True)
    type = sql.Column(sql.String, nullable=False)

    samples = relationship(
        "Sample", secondary=sample_string_association, back_populates="strings"
    )

    def __init__(
        self, value: str, type: str, sha256: str = None
    ) -> String:

        if not sha256:
            sha256 = hashlib.sha256(value.encode("utf-8")).hexdigest()

        self.value = value
        self.sha256 = sha256
        self.type = type
