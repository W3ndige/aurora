from tests.utils import upload_file

def test_add_sample(client, monkeypatch):
    def mock_push_sample(a, b, c):
        return None

    def mock_push_ssdeep(a, b, c):
        return None

    monkeypatch.setattr("aurora.core.karton.push_file", mock_push_sample)
    monkeypatch.setattr("aurora.core.karton.push_ssdeep", mock_push_ssdeep)

    file = upload_file()
    response = client.post("/api/v1/sample/", files={'file': (file["filename"], file["content"])}).json()

    assert response["filename"] == file["filename"]
    assert response["sha256"] == file["sha256"]
    assert response["filesize"] == len(file["content"])