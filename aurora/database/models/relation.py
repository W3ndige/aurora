from __future__ import annotations

import enum
import sqlalchemy as sql

from sqlalchemy.orm import relationship, backref

from aurora.database import Base


class RelationType(str, enum.Enum):
    ASCII_STRINGS = "ASCII_STRINGS"
    WIDE_STRINGS = "WIDE_STRINGS"
    STRING = "STRING"
    SSDEEP = "SSDEEP"


class RelationConfidence(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Relation(Base):
    __tablename__ = "relation"

    id = sql.Column(sql.Integer, primary_key=True)
    parent_id = sql.Column(sql.Integer, sql.ForeignKey("sample.id"), nullable=False)
    child_id = sql.Column(sql.Integer, sql.ForeignKey("sample.id"), nullable=False)
    relation_type = sql.Column(sql.Enum(RelationType), nullable=False)
    confidence = sql.Column(sql.Enum(RelationConfidence), nullable=False)

    sql.UniqueConstraint("parent_id", "child_id", "relation_type")

    parent = relationship(
        "Sample", foreign_keys=[parent_id], backref=backref("related_children")
    )
    child = relationship(
        "Sample", foreign_keys=[child_id], backref=backref("related_parents")
    )
