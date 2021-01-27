from __future__ import annotations

import sqlalchemy as sql

from sqlalchemy.orm import relationship

from aurora.database import Base

sample_string_association = sql.Table(
    'sample_string_association',
    Base.metadata,
    sql.Column('sample_id', sql.Integer, sql.ForeignKey('sample.id')),
    sql.Column('string_id', sql.Integer, sql.ForeignKey('string.id')),
    sql.UniqueConstraint("sample_id", "string_id", name="unique_sample_string")
)


class String(Base):
    __tablename__ = "string"

    id = sql.Column(sql.Integer, primary_key=True)
    type = sql.Column(sql.String(5), index=True, nullable=False)
    value = sql.Column(sql.String, index=True, unique=True, nullable=False)
    status = sql.Column(sql.String(10), index=True, nullable=False)

    samples = relationship(
        "Sample",
        secondary=sample_string_association,
        back_populates="strings"
    )
