from __future__ import annotations

import sqlalchemy as sql
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import BYTEA

from aurora.database import Base, ANALYSIS_TYPE


class Minhash(Base):
    __tablename__ = "minhash"

    id = sql.Column(sql.Integer, primary_key=True)
    sample_id = sql.Column(sql.Integer, sql.ForeignKey("sample.id"))
    minhash = sql.Column(BYTEA, nullable=False)
    analysis_type = sql.Column(ANALYSIS_TYPE, nullable=False, index=True)

    sample = relationship("Sample")
