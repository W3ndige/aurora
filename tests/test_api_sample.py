from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from aurora.app import app
from aurora.database import Base, get_db

engine = create_engine(
    "postgresql://postgres:postgres@postgres:5432/aurora_test"
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_add_sample(monkeypatch):
    filepath = "tests/testdata/random_262144_deea51994761de54aff0ef112ace7ce41503d8893998817e5801ae21a88cac7c"
    filename = filepath.split("/")[2]
    sha256 = filename.split("_")[2]
    size = int(filename.split("_")[1])

    def mock_push_sample(a, b, c):
        return None

    def mock_push_ssdeep(a, b, c):
        return None

    monkeypatch.setattr("aurora.core.karton.push_file", mock_push_sample)
    monkeypatch.setattr("aurora.core.karton.push_ssdeep", mock_push_ssdeep)

    with open(filepath, "rb") as random_file:
        response = client.post("/api/v1/sample/", files={'file': random_file}).json()

        assert response["filename"] == filename
        assert response["sha256"] == sha256
        assert response["filesize"] == size