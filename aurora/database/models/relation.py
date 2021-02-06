from __future__ import annotations

import sqlalchemy as sql
from sqlalchemy.orm import relationship, backref

from aurora.database import Base


class Relation(Base):
    __tablename__ = "relation"

    id = sql.Column(sql.Integer, primary_key=True)
    parent_id = sql.Column(sql.Integer, sql.ForeignKey("sample.id"), nullable=False)
    child_id = sql.Column(sql.Integer, sql.ForeignKey("sample.id"), nullable=False)
    type = sql.Column(sql.String, nullable=False)
    strength = sql.Column(sql.Integer, nullable=False, default=0)
    occurance_count = sql.Column(sql.Integer, nullable=False, default=0)
    trait = sql.Column(sql.String)

    sql.UniqueConstraint(parent_id, child_id, type, name="unique_parent_child_of_type")

    parent = relationship(
        "Sample",
        foreign_keys=[parent_id],
        backref=backref("children_samples")
    )

    child = relationship(
        "Sample",
        foreign_keys=[child_id],
        backref=backref("parent_samples")
    )
