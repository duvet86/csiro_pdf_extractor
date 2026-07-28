import os
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, status

from docling.datamodel.base_models import InputFormat
from docling.document_extractor import DocumentExtractor
from docling.document_converter import DocumentConverter

extractor = DocumentExtractor(allowed_formats=[InputFormat.IMAGE, InputFormat.PDF])

# Initialize the router with specific configuration (optional)
router = APIRouter(
    prefix="/advanced-extraction"
)

@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def extract_pdf_fields_docling(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Extract key fields from an energy bill PDF using docling for text extraction."""
    is_pdf_mime = file.content_type == "application/pdf"
    is_pdf_filename = bool(file.filename and file.filename.lower().endswith(".pdf"))
    if not (is_pdf_mime or is_pdf_filename):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a PDF file.",
        )

    try:
        task_id = "1"
        background_tasks.add_task(heavy_computation_task, task_id, file)

        return {
            "status": "Accepted",
            "message": "Task received and queued for processing.",
            "task_id": task_id,
            "poll_url": f"/tasks/{task_id}"
        }

        # try:
        #     converter = DocumentConverter()
        #     result = converter.convert(tmp_path)
        #     full_text = result.document.export_to_markdown()
        # finally:
        #     os.unlink(tmp_path)

        # # fields = _extract_pdf_key_fields(full_text)

        # return {
        #     "filename": file.filename,
        #     # "extracted_fields": fields,
        # }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the PDF: {str(e)}",
        )

async def heavy_computation_task(task_id: str, file: UploadFile):
    pdf_bytes = await file.read()
    # Docling requires a file path, so write to a named temp file
    suffix = os.path.splitext(file.filename or "bill.pdf")[1] or ".pdf"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    try:
        extracted = extractor.extract(
            source=tmp_path,
            template='{"bill_no": "string", "total": "float"}',
        )

        print(f"Task {task_id} completed. Extracted data: {extracted}")
    finally:
        os.unlink(tmp_path)