from __future__ import annotations

import sqlalchemy as sql
from sqlalchemy.orm import relationship, backref

from aurora.database import Base, ANALYSIS_TYPE


class Relation(Base):
    __tablename__ = "relation"

    id = sql.Column(sql.Integer, primary_key=True)
    parent_id = sql.Column(sql.Integer, sql.ForeignKey("sample.id"), nullable=False)
    child_id = sql.Column(sql.Integer, sql.ForeignKey("sample.id"), nullable=False)
    relation_type = sql.Column(ANALYSIS_TYPE, nullable=False)
    confidence = sql.Column(sql.String, nullable=False)

    parent = relationship(
        "Sample", foreign_keys=[parent_id], backref=backref("related_children")
    )
    child = relationship(
        "Sample", foreign_keys=[child_id], backref=backref("related_parents")
    )
