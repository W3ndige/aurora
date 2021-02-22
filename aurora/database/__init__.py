from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from aurora import config


engine: Engine = create_engine(config.POSTGRES_URI)

db_session: sessionmaker = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base(name="Base")

from .models import Relation  # noqa E402, E401
from .models import Sample  # noqa E402, E401
from .models import Minhash  # noqa E402, E401
from .models import SsDeep  # noqa E402, E401

def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()


__all__ = ["db_session", "get_db", "Base"]
