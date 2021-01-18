from __future__ import annotations

from typing import List
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Column, Integer, String, ForeignKey

from aurora.database import Base


class Feature(Base):
    __tablename__ = "feature"

    id = Column(Integer, primary_key=True)
    sample_id = Column(Integer, (ForeignKey("sample.id")))
    type = Column(String, nullable=False, index=True)
    data = Column(ARRAY(String), nullable=False)

    UniqueConstraint("sample_id", "type", name="unique_type")

    @staticmethod
    def from_list(data: List, type: str) -> Feature:
        return Feature(
            type=type,
            data=data
        )
