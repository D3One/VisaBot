from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_us_visa_apply_and_status() -> None:
    payload = {
        "user_id": "12345",
        "chat_id": 987654321,
        "surname": "Miller",
        "given_name": "Anna",
        "passport_number": "C1234567",
        "birth_date": "1992-05-12",
        "arrival_date": "2026-09-15",
        "stay_length": 30,
        "purpose": "tourism",
    }
    response = client.post("/api/v1/us-visa/apply", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["application_number"].startswith("US-DRYRUN-")
    assert body["screenshot_base64"]

    status_response = client.get(f"/api/v1/us-visa/status/{body['application_number']}")
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "DRAFT_CREATED"


def test_us_visa_apply_requires_chat_id() -> None:
    payload = {
        "user_id": "12345",
        "surname": "Miller",
        "given_name": "Anna",
        "passport_number": "C1234567",
        "birth_date": "1992-05-12",
        "arrival_date": "2026-09-15",
        "stay_length": 30,
        "purpose": "tourism",
    }
    response = client.post("/api/v1/us-visa/apply", json=payload)
    assert response.status_code == 422


def test_schengen_apply_and_status() -> None:
    payload = {
        "user_id": "12345",
        "chat_id": 987654321,
        "target_country": "germany",
        "surname": "Miller",
        "given_name": "Anna",
        "passport_number": "C1234567",
        "birth_date": "1992-05-12",
        "arrival_date": "2026-09-15",
        "stay_length": 14,
        "purpose": "tourism",
        "address": "Musterstrasse 12",
        "city": "Berlin",
        "zip_code": "10115",
        "phone": "+4915112345678",
        "email": "anna.mueller@example.com",
    }
    response = client.post("/api/v1/schengen/apply", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["application_number"].startswith("SCH-DRYRUN-")
    assert body["pdf_base64"]

    status_response = client.get(f"/api/v1/schengen/status/{body['application_number']}")
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "DRAFT_CREATED"


def test_mock_us_visa_apply_and_status() -> None:
    payload = {
        "user_id": "test_user_1",
        "chat_id": 987654321,
        "surname": "Doe",
        "given_name": "John",
        "passport_number": "A1234567",
        "birth_date": "1990-01-01",
        "arrival_date": "2026-07-15",
        "stay_length": "30",
        "purpose": "tourism",
    }
    response = client.post("/api/v1/mock/us-visa/apply", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["application_number"].startswith("US")
    assert body["status"] == "PENDING"

    status_response = client.get(f"/api/v1/mock/status/{body['application_number']}")
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "PENDING"


def test_mock_us_visa_rejects_bad_passport() -> None:
    payload = {
        "user_id": "test_user_1",
        "chat_id": 987654321,
        "surname": "Doe",
        "given_name": "John",
        "passport_number": "!!!",
        "birth_date": "1990-01-01",
        "arrival_date": "2026-07-15",
        "stay_length": "30",
        "purpose": "tourism",
    }
    response = client.post("/api/v1/mock/us-visa/apply", json=payload)
    assert response.status_code == 422


def test_mock_schengen_apply_and_status() -> None:
    payload = {
        "user_id": "test_user_2",
        "chat_id": 987654321,
        "target_country": "germany",
        "surname": "Doe",
        "given_name": "Jane",
        "passport_number": "B1234567",
        "birth_date": "1991-02-02",
        "nationality": "DE",
        "passport_issuing_country": "DE",
        "passport_expiration": "2030-12-31",
        "address": "Musterstrasse 12",
        "city": "Berlin",
        "zip_code": "10115",
        "country": "DE",
        "phone": "+4915112345678",
        "email": "jane.doe@example.com",
        "purpose": "tourism",
        "arrival_date": "2026-09-15",
        "stay_length": "14",
        "occupation": "student",
    }
    response = client.post("/api/v1/mock/schengen/apply", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["application_number"].startswith("DE")
    assert body["status"] == "PENDING"

    status_response = client.get(f"/api/v1/mock/status/{body['application_number']}")
    assert status_response.status_code == 200
    assert status_response.json()["type"] == "SCHENGEN"
