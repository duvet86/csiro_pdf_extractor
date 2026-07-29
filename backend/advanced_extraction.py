from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, status
from io import BytesIO

from docling.datamodel.base_models import InputFormat
from docling.document_extractor import DocumentExtractor
from docling.datamodel.base_models import DocumentStream

from data.database import ExtractedData, Job, SessionDep

extractor = DocumentExtractor(allowed_formats=[InputFormat.IMAGE, InputFormat.PDF])

router = APIRouter(
    prefix="/advanced-extraction"
)

@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def extract_pdf_fields_docling(session: SessionDep, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Extract key fields from an energy bill PDF using docling for text extraction."""
    is_pdf_mime = file.content_type == "application/pdf"
    is_pdf_filename = bool(file.filename and file.filename.lower().endswith(".pdf"))
    if not (is_pdf_mime or is_pdf_filename):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a PDF file.",
        )

    try:
        job = Job(file_name=file.filename or "bill.pdf", num_pages=0, status="pending")

        session.add(job)
        session.commit()
        session.refresh(job)

        if not job.id:
            raise HTTPException(
                status_code=500,
                detail="Failed to create job entry in the database.",
            )

        pdf_bytes = await file.read()

        background_tasks.add_task(extract_data, session, job.id, pdf_bytes)

        return {
            "status": "Accepted",
            "message": "Task received and queued for processing.",
            "task_id": job.id,
            "poll_url": f"/jobs/{job.id}"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the PDF: {str(e)}",
        )

def extract_data(session: SessionDep, job_id: int, pdf_bytes: bytes):
    print(f"Starting heavy computation task for job_id: {job_id}")  

    buf = BytesIO(pdf_bytes)
    source = DocumentStream(name="my_doc.pdf", stream=buf)

    extracted = extractor.extract(
        source=source,
        template='{"retailer": "string", "billing_period": "string", "total_cost": "float", "total_usage_kWh": "float"}',
    )

    job = session.get(Job, job_id)
    if not job:
        raise Exception(f"Job with ID {job_id} not found in the database.")

    job.num_pages = len(extracted.pages) if extracted.pages else 0

    for i, (key, value) in enumerate(extracted.model_dump(), start=1):
        if value is not None:
            session.add(
                ExtractedData(
                    page_number=i,
                    key=key,
                    value=value,
                    job=job
                )
            )

    job.status = "success"

    session.commit()

    print(f"Completed heavy computation task for job_id: {job_id}")