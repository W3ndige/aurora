import random

from tests.utils import upload_file


def test_add_relation(client, monkeypatch):
    file_1 = upload_file(content="File_1")
    file_2 = upload_file(content="File_2")

    def mock_push_sample(a, b, c):
        return None

    def mock_push_ssdeep(a, b, c):
        return None

    monkeypatch.setattr("aurora.core.karton.push_file", mock_push_sample)
    monkeypatch.setattr("aurora.core.karton.push_ssdeep", mock_push_ssdeep)

    parent_response = client.post(
        "/api/v1/sample/", files={"file": (file_1["filename"], file_1["content"])}
    ).json()
    parent_id = parent_response["id"]

    child_response = client.post(
        "/api/v1/sample/", files={"file": (file_2["filename"], file_2["content"])}
    ).json()
    child_id = child_response["id"]

    relation = {
        "parent_sha256": file_1["sha256"],
        "child_sha256": file_2["sha256"],
        "type": "test",
        "confidence": random.uniform(0.0, 1.0),
    }

    response = client.post("/api/v1/relation/", json=relation).json()

    assert response["parent_id"] == parent_id
    assert response["child_id"] == child_id
    assert response["confidence"] == relation["confidence"]


def test_add_relation_invalid_confidence(client):
    file_1 = upload_file(content="File_1")
    file_2 = upload_file(content="File_2")

    relation = {
        "parent_sha256": file_1["sha256"],
        "child_sha256": file_2["sha256"],
        "type": "test",
        "confidence": 1.1,
    }

    response = client.post("/api/v1/relation/", json=relation)

    assert response.status_code == 400


def test_relation_by_parent(client):
    file_1 = upload_file(content="File_1")
    file_2 = upload_file(content="File_2")

    file_2_id = client.get(f"/api/v1/sample/{file_2['sha256']}").json()["id"]

    response = client.get(f"/api/v1/relation/parent/{file_1['sha256']}").json()

    assert len(response) == 1
    assert response[0]["child_id"] == file_2_id


def test_relation_by_child(client):
    file_1 = upload_file(content="File_1")
    file_2 = upload_file(content="File_2")

    file_1_id = client.get(f"/api/v1/sample/{file_1['sha256']}").json()["id"]

    response = client.get(f"/api/v1/relation/child/{file_2['sha256']}").json()

    assert len(response) == 1
    assert response[0]["parent_id"] == file_1_id
