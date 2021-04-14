from tests.utils import upload_file, add_minhash, add_string


def test_add_sample(client, monkeypatch):
    def mock_push_sample(a, b, c):
        return None

    def mock_push_ssdeep(a, b, c):
        return None

    monkeypatch.setattr("aurora.core.karton.push_file", mock_push_sample)
    monkeypatch.setattr("aurora.core.karton.push_ssdeep", mock_push_ssdeep)

    file = upload_file()
    response = client.post(
        "/api/v1/sample/", files={"file": (file["filename"], file["content"])}
    ).json()

    assert response["filename"] == file["filename"]
    assert response["sha256"] == file["sha256"]
    assert response["filesize"] == len(file["content"])


def test_get_sample(client):
    file = upload_file()

    response = client.get(f"/api/v1/sample/{file['sha256']}").json()

    assert response["filename"] == file["filename"]
    assert response["sha256"] == file["sha256"]
    assert response["filesize"] == len(file["content"])


def test_add_minhash(client):
    file = upload_file()
    minhash = add_minhash()
    minhash.update({"minhash_type": "strings"})

    response = client.post(
        f"api/v1/sample/{file['sha256']}/minhash", json=minhash
    ).json()

    assert response["minhash_type"] == minhash["minhash_type"]
    assert response["seed"] == minhash["seed"]
    assert response["hash_values"] == minhash["hash_values"]


def test_get_sample_minhashes(client):
    file = upload_file()

    response = client.post(f"api/v1/sample/{file['sha256']}/minhash").json()

    assert len(response) == 1


def test_add_minhash_unknown_sample(client):
    # Unknown file
    file = upload_file(content="Unknown content")
    minhash = add_minhash()
    minhash.update({"minhash_type": "strings"})

    response = client.post(f"api/v1/sample/{file['sha256']}/minhash", json=minhash)

    assert response.status_code == 404


def test_get_ssdeep(client):
    file = upload_file()

    response = client.get(f"/api/v1/sample/{file['sha256']}/ssdeep").json()

    assert response["ssdeep"] == file["ssdeep"]


def test_add_string(client):
    file = upload_file()
    string = add_string()

    response = client.post(f"api/v1/sample/{file['sha256']}/string", json=string).json()

    assert response["value"] == string["value"]
    assert response["sha256"] == string["sha256"]
    assert response["heuristic"] == string["heuristic"]


def test_add_string_incorrect_sha256(client):
    file = upload_file()
    string = add_string()
    modified_string = add_string(string="Modified string")

    modified_string["value"] = string["value"]

    response = client.post(
        f"api/v1/sample/{file['sha256']}/string", json=modified_string
    ).json()

    assert response["value"] == string["value"]
    assert response["sha256"] == string["sha256"]
    assert response["heuristic"] == string["heuristic"]
