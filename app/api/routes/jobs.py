from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.job import GenerationJob
from app.models.recipient import Recipient
from app.schemas.job import GenerationJobCreate
from app.services.job_service import process_job

router = APIRouter(
    prefix="/api/jobs",
    tags=["Jobs"]
)

# api that creates a bulk certificate generation job
@router.post("/")
def create_job(
    job_data: GenerationJobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    job = GenerationJob(
        event_name=job_data.event_name,
        issue_date=job_data.issue_date,
        total_recipients=len(job_data.recipients)
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    for recipient_data in job_data.recipients:
        recipient = Recipient(
            job_id=job.id,
            name=recipient_data.name,
            email=recipient_data.email
        )

        db.add(recipient)

    db.commit()

    background_tasks.add_task(process_job, job.id)

    return {
        "job_id": job.id,
        "status": job.status,
        "total_recipients": job.total_recipients
    }

# api: checks the status and progress of a certificate generation job
@router.get("/{job_id}")
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.get(GenerationJob, job_id)

    if not job:
        return {
            "message": "Job not found"
        }

    return {
        "job_id": job.id,
        "event_name": job.event_name,
        "issue_date": job.issue_date,
        "status": job.status,
        "total_recipients": job.total_recipients,
        "successful_count": job.successful_count,
        "failed_count": job.failed_count,
        "completed_at": job.completed_at
    }