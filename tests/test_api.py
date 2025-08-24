from fastapi.testclient import TestClient

from src.whisper_api.api import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "whisper_model" in data


def test_transcribe_endpoint_no_file() -> None:
    response = client.post("/transcribe")
    assert response.status_code == 422


def test_transcribe_endpoint_invalid_file() -> None:
    response = client.post(
        "/transcribe",
        files={"audio_file": ("test.txt", b"invalid content", "text/plain")},
    )
    assert response.status_code == 400
