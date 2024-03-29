"""Models for storing Minhashes.

This module describes a model for storing Minhash values.
"""

from __future__ import annotations

import sqlalchemy as sql

from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from aurora.database import Base


if TYPE_CHECKING:
    from aurora.database.models import Sample  # noqa: F401


class Minhash(Base):

    __tablename__ = "minhash"

    id = sql.Column(sql.Integer, primary_key=True)
    sample_id = sql.Column(sql.Integer, sql.ForeignKey("sample.id"))
    seed = sql.Column(sql.BIGINT, nullable=False)
    hash_values = sql.Column(sql.ARRAY(sql.BIGINT()), nullable=False)
    minhash_type = sql.Column(sql.String, nullable=False, index=True)
    extra_data = sql.Column(JSONB)

    sql.UniqueConstraint("sample_id", "analysis_type", name="unique_analysis_sample")

    sample = relationship("Sample", back_populates="minhashes")
