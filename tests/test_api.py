from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.database.db import SessionLocal
from app.models.recipient import Recipient
from app.services import job_service
from app.services.certificate_service import generate_certificate

client = TestClient(app)

#Testcase 1 :new bulk certificate generation job can be created
def test_create_generation_job():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Test Workshop",
            "issue_date": "2026-10-08",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "test@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "job_id" in data
    assert data["total_recipients"] == 1

# Testcase 2: invalid recipient data is rejected by the API
def test_input_validation():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Test Workshop",
            "issue_date": "2026-10-08",
            "recipients": [
                {
                    "name": "A",
                    "email": "invalid-email"
                }
            ]
        }
    )

    assert response.status_code == 422

# Testcase 3: It tests that a certificate PDF is generated successfully
def test_certificate_generation():
    file_path = generate_certificate(
        recipient_name="Test User",
        event_name="Test Workshop",
        issue_date="2026-10-08",
        recipient_id=999999
    )

    path = Path(file_path)

    assert path.exists()
    assert path.suffix == ".pdf"

    path.unlink()

# Testcase 4: the job status API returns correct progress and completion details
def test_job_status():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Status Test",
            "issue_date": "2026-10-08",
            "recipients": [
                {
                    "name": "Status User",
                    "email": "status@example.com"
                }
            ]
        }
    )

    job_id = response.json()["job_id"]

    response = client.get(f"/api/jobs/{job_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["job_id"] == job_id
    assert data["total_recipients"] == 1
    assert data["successful_count"] == 1
    assert data["failed_count"] == 0
    assert data["status"] == "COMPLETED"

# Testcase 5: one failed certificate does not stop other certificates in the same job
def test_individual_certificate_failure(monkeypatch):
    def fake_generate_certificate(
        recipient_name,
        event_name,
        issue_date,
        recipient_id
    ):
        if recipient_name == "Failed User":
            raise Exception("Certificate generation failed")

        return "generated_certificates/test_success.pdf"

    monkeypatch.setattr(
        job_service,
        "generate_certificate",
        fake_generate_certificate
    )

    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Failure Test",
            "issue_date": "2026-10-08",
            "recipients": [
                {
                    "name": "Successful User",
                    "email": "success@example.com"
                },
                {
                    "name": "Failed User",
                    "email": "failed@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    job_id = response.json()["job_id"]

    response = client.get(f"/api/jobs/{job_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["successful_count"] == 1
    assert data["failed_count"] == 1
    assert data["status"] == "PARTIAL"

# Testcase 6: a successfully generated certificate can be retrieveed as a PDF
def test_retrieve_generated_certificate():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Retrieval Test",
            "issue_date": "2026-10-08",
            "recipients": [
                {
                    "name": "Certificate User",
                    "email": "certificate@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    job_id = response.json()["job_id"]

    db = SessionLocal()

    recipient = (
        db.query(Recipient)
        .filter(Recipient.job_id == job_id)
        .first()
    )

    recipient_id = recipient.id

    db.close()

    response = client.get(
        f"/api/certificates/{recipient_id}"
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"