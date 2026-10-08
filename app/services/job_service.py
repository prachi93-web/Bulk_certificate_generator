from datetime import datetime
from app.database.db import SessionLocal
from app.models.job import GenerationJob
from app.models.recipient import Recipient
from app.services.certificate_service import generate_certificate

def process_job(job_id: int):
    db = SessionLocal()
    try:
        job = db.get(GenerationJob, job_id)

        if not job:
            return

        job.status = "PROCESSING"
        db.commit()

        recipients = (
            db.query(Recipient)
            .filter(Recipient.job_id == job_id)
            .all()
        )

        for recipient in recipients:
            try:
                recipient.status = "PROCESSING"
                db.commit()

                certificate_path = generate_certificate(
                    recipient_name=recipient.name,
                    event_name=job.event_name,
                    issue_date=str(job.issue_date),
                    recipient_id=recipient.id
                )

                recipient.status = "SUCCESS"
                recipient.certificate_path = certificate_path
                job.successful_count += 1

            except Exception as error:
                recipient.status = "FAILED"
                recipient.error_message = str(error)
                job.failed_count += 1

            db.commit()

        if job.failed_count == 0:
            job.status = "COMPLETED"
        elif job.successful_count == 0:
            job.status = "FAILED"
        else:
            job.status = "PARTIAL"

        job.completed_at = datetime.utcnow()
        db.commit()

    finally:
        db.close()