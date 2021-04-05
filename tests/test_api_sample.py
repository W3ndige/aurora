from fastapi.testclient import TestClient

from aurora.app import app
from aurora.database import get_db

from .utils import override_get_db, get_test_sample, get_random_minhash

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

filepath, filename, sha256, size = get_test_sample()

def test_add_sample(monkeypatch):
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


def test_get_sample():
    response = client.get(f"/api/v1/sample/{sha256}")

    assert response["filename"] == filename
    assert response["sha256"] == sha256
    assert response["filesize"] == size



def test_add_sample_minhash():
    seed, hash_values = get_random_minhash()

    response = client.post(f"/api/v1/sample/{sha256}", json={"seed": seed, "hash_values": hash_values, "minhash_type": "STRINGS"})

    assert response["seed"] == seed
    assert response["hash_values"] == hash_values


def test_add_duplicate_sample_minhash():
    seed, hash_values = get_random_minhash()

    response = client.post(f"/api/v1/sample/{sha256}", json={"seed": seed, "hash_values": hash_values, "minhash_type": "STRINGS"})

    assert response["seed"] == seed
    assert response["hash_values"] == hash_values