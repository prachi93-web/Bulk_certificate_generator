# Bulk Certificate Generator API

A FastAPI backend for generating certificates in bulk from a predefined certificate template.

The API accepts multiple recipients in a single request, validates their data, generates individual certificates, tracks job progress, handles individual failures, and allows generated certificates to be retrieved.

## Features

- Bulk certificate generation
- Recipient validation
- Predefined certificate template
- Background processing
- Job status and progress tracking
- Individual success/failure tracking
- Certificate PDF retrieval
- SQLite database
- Automated tests

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- ReportLab
- Pytest
- HTTPX

## Project Structure

```text
Bulk_certificate_generator/
│
├── app/
│   ├── api/routes/
│   │   ├── jobs.py
│   │   └── certificates.py
│   ├── database/
│   │   └── db.py
│   ├── models/
│   │   ├── job.py
│   │   └── recipient.py
│   ├── schemas/
│   │   └── job.py
│   ├── services/
│   │   ├── certificate_service.py
│   │   └── job_service.py
│   └── main.py
│
├── generated_certificates/
├── templates/
│   └── certificate_template.png
├── tests/
│   └── test_api.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/prachi93-web/Bulk_certificate_generator.git
cd Bulk_certificate_generator
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
```

Windows PowerShell:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

The SQLite database is created automatically when the application starts.

## API Endpoints

### 1. Create Bulk Generation Job

```http
POST /api/jobs/
```

Creates a generation job for multiple recipients.

Example request:

```json
{
  "event_name": "Python Workshop",
  "issue_date": "2026-10-08",
  "recipients": [
    {
      "name": "John Doe",
      "email": "john@example.com"
    },
    {
      "name": "Jane Doe",
      "email": "jane@example.com"
    }
  ]
}
```

Example response:

```json
{
  "job_id": 1,
  "status": "QUEUED",
  "total_recipients": 2
}
```

### 2. Check Job Status

```http
GET /api/jobs/{job_id}
```

Returns the generation status and progress.

Example response:

```json
{
  "job_id": 1,
  "event_name": "Python Workshop",
  "issue_date": "2026-10-08",
  "status": "COMPLETED",
  "total_recipients": 2,
  "successful_count": 2,
  "failed_count": 0,
  "completed_at": "2026-10-08T12:00:00"
}
```

Possible statuses:

- `QUEUED`
- `PROCESSING`
- `COMPLETED`
- `PARTIAL`
- `FAILED`

### 3. Retrieve Certificate

```http
GET /api/certificates/{recipient_id}
```

Retrieves the generated certificate as a PDF.

The certificate is available when the recipient status is `SUCCESS`.

## Validation and Failure Handling

Pydantic validates:

- Recipient name
- Email
- Event name
- Issue date
- At least one recipient

Invalid data returns HTTP `422`.

Each recipient is processed independently. If one certificate fails, it is marked as `FAILED` and processing continues for the remaining recipients.

For example:

```text
Total: 10
Successful: 9
Failed: 1
Status: PARTIAL
```

## Certificate Generation

ReportLab is used to generate the certificates.

A predefined template is used as the background, with the following information added dynamically:

- Recipient name
- Event name
- Issue date

Generated certificates are stored in:

```text
generated_certificates/
```

## Background Processing

FastAPI `BackgroundTasks` is used for certificate generation.

The flow is:

```text
POST /api/jobs/
       ↓
Create job and recipients
       ↓
Background certificate generation
       ↓
Update job status
       ↓
Retrieve generated certificate
```

BackgroundTasks was selected because the project is lightweight and does not require additional infrastructure such as Celery or Redis.

## Testing

The project contains 6 automated tests using Pytest.

Tests cover:

1. Job creation
2. Input validation
3. Certificate generation
4. Job status
5. Individual certificate failure
6. Certificate retrieval

Run tests with:

```bash
python -m pytest
```

Expected result:

```text
6 passed
```

## Database

SQLite with SQLAlchemy is used as the relational database.

The application maintains two main tables:

- `generation_jobs` - stores bulk generation job information and progress
- `recipients` - stores recipient details, certificate status, file path, and errors

One generation job can contain multiple recipients.

## Design Decisions

### SQLite

SQLite was selected because it is simple to set up and does not require a separate database server.

### BackgroundTasks

FastAPI BackgroundTasks keeps the implementation simple while allowing certificate generation to happen after the job request is accepted.

### Failure Isolation

Each recipient is processed independently so that one failed certificate does not stop the entire bulk job.

## Assignment Coverage

The implementation covers:

- Bulk certificate generation
- Recipient validation
- Predefined certificate template
- Relational database
- Background processing
- Job status tracking
- Success/failure tracking
- Individual failure handling
- Certificate retrieval
- Automated tests