from datetime import date, datetime
from sqlalchemy import Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.db import Base

class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    event_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    issue_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="QUEUED"
    )

    total_recipients: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    successful_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    failed_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )