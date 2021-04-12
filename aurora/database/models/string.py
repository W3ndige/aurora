import sqlalchemy as sql

from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship

from aurora.database import Base

if TYPE_CHECKING:
    from aurora.database.models import Sample  # noqa: F401


class String(Base):
    __tablename__ = "string"

    id = sql.Column(sql.Integer, primary_key=True)
    sample_id = sql.Column(sql.Integer, sql.ForeignKey("sample.id"))
    value = sql.Column(sql.String, nullable=False)
    sha256 = sql.Column(sql.String(64), nullable=False, index=True)
    heuristic = sql.Column(sql.String, nullable=False)

    sql.UniqueConstraint("sample_id", "sha256", "unique_string")

    sample = relationship("Sample")
