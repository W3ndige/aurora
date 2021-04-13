import pytest

from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

from aurora.app import app
from aurora.database import get_db, Base
from aurora.config import DATABASE_URL, POSTGRES_DB

engine = create_engine(
    DATABASE_URL
)

DB_URL = f"{DATABASE_URL}_test"

with engine.connect() as default_conn:
    default_conn.execution_options(isolation_level="AUTOCOMMIT").execute(f"DROP DATABASE IF EXISTS {POSTGRES_DB}_test")
    default_conn.execution_options(isolation_level="AUTOCOMMIT").execute(f"CREATE DATABASE {POSTGRES_DB}_test")

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def db_fixture() -> Session:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def client(db_fixture) -> TestClient:
    def _get_db_override():
        return db_fixture

    app.dependency_overrides[get_db] = _get_db_override
    return TestClient(app)