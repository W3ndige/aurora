from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from .utils import recreate_db

POSTGRES_URL = 'postgres+psycopg2://postgres:postgres@localhost:5432/postgres'

engine: Engine = create_engine(
    POSTGRES_URL
)

db_session: Session = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base(name='Base')

# Useful ENUMs

ANALYSIS_TYPE = ENUM(
    "ASCII_STRINGS", "WIDE_STRINGS", "YARA", name="analysis_type"
)

from .models import Relation    # noqa E402, E401
from .models import Sample      # noqa E402, E401
from .models import Minhash     # noqa E402, E401

recreate_db(Base, engine)


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()


__all__ = [
    "db_session",
    "get_db",
    "Base",
    "ANALYSIS_TYPE"
]
