from fastapi import FastAPI
from app.database.db import Base, engine
from app.models.job import GenerationJob
from app.models.recipient import Recipient
from app.api.routes.jobs import router as jobs_router
from app.api.routes.certificates import router as certificates_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bulk Certificate Generator API",
    description="Backend API for generating certificates in bulk.",
    version="1.0.0"
)

app.include_router(jobs_router)
app.include_router(certificates_router)

@app.get("/")
def root():
    return {
        "message": "Bulk Certificate Generator API is running"
    }