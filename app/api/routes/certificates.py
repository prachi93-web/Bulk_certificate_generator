from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.recipient import Recipient

router = APIRouter(
    prefix="/api/certificates",
    tags=["Certificates"]
)

# api to retrieve a successfully generated certificate as a pdf
@router.get("/{recipient_id}")
def get_certificate(
    recipient_id: int,
    db: Session = Depends(get_db)
):
    recipient = db.get(Recipient, recipient_id)

    if not recipient:
        raise HTTPException(
            status_code=404,
            detail="Recipient not found"
        )

    if recipient.status != "SUCCESS":
        raise HTTPException(
            status_code=404,
            detail="Certificate is not available"
        )

    file_path = Path(recipient.certificate_path)

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Certificate file not found"
        )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=file_path.name
    )