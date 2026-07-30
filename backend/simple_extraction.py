from fastapi import APIRouter, UploadFile, File, HTTPException
import io
import re
from pypdf import PdfReader

from data.database import Job, ExtractedData, SessionDep

router = APIRouter(
    prefix="/simple-extraction"
)

@router.post("")
async def extract_pdf_text(session: SessionDep, file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Please upload a PDF file."
        )
    
    try:
        pdf_bytes = await file.read()
        
        pdf_stream = io.BytesIO(pdf_bytes)
        reader = PdfReader(pdf_stream)

        job = Job(file_name=file.filename or "bill.pdf", num_pages=len(reader.pages), extraction_mode = "simple", status="success")
        session.add(job)
        
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            extracted_data = _extract_pdf_key_fields(text)
            for key, value in extracted_data.items():
                if value is not None:
                    session.add(
                        ExtractedData(
                            page_number=page_num,
                            key=key,
                            value=str(value),
                            job=job
                        )
                    )

        session.commit()
            
        return {
            "filename": file.filename,
            "total_pages": len(reader.pages),
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred while processing the PDF: {str(e)}"
        )

def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def _extract_retailer(text: str) -> str | None:
    label_patterns = [
        r"(?:retailer|energy\s+retailer|issued\s+by|sold\s+by)\s*[:\-]\s*([A-Za-z][A-Za-z0-9&.,'()\-\s]{2,80})",
        r"(?:retailer|energy\s+retailer)\s+([A-Za-z][A-Za-z0-9&.,'()\-\s]{2,80})",
        r"(?i)\b(Synergy|AGL|Origin(?:\s+Energy)?|Alinta(?:\s+Energy)?|Red\s+Energy|Powershop|EnergyAustralia|Simply\s+Energy)\b"
    ]
    for pattern in label_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return _normalize_whitespace(match.group(1))
    return None


def _extract_billing_period(text: str) -> str | None:
    label_patterns = [
        r"(?:billing|bill)\s*(?:period|cycle)\s*[:\-]\s*([^\n]{5,80})",
        r"(?:for\s+the\s+period)\s*[:\-]?\s*([^\n]{5,80})",
    ]
    for pattern in label_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return _normalize_whitespace(match.group(1))

    range_patterns = [
        r"(\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b\s*(?:to|-|–|—)\s*\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b)",
        r"(\b\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4}\b\s*(?:to|-|–|—)\s*\b\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4}\b)",
    ]
    for pattern in range_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return _normalize_whitespace(match.group(1))
    return None


def _extract_total_cost(text: str) -> float | None:
    patterns = [
        r"(?:total\s*(?:amount\s*due|cost|charges?|bill)?|amount\s*due)\s*[:\-]?\s*\$?\s*([0-9][0-9,]*(?:\.[0-9]{2})?)",
        r"\$\s*([0-9][0-9,]*(?:\.[0-9]{2})?)\s*(?:total\s*(?:amount\s*due|cost|charges?|bill)|amount\s*due)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            try:
                return float(match.group(1).replace(",", ""))
            except ValueError:
                continue
    return None


def _extract_total_usage_kwh(text: str) -> float | None:
    patterns = [
        r"(?:total\s*(?:usage|energy|electricity|consumption)|usage)\s*(?:\(?(?:kwh|kw\.h)\)?)?\s*[:\-]?\s*([0-9][0-9,]*(?:\.[0-9]+)?)\s*(?:kwh|kw\.h)?",
        r"([0-9][0-9,]*(?:\.[0-9]+)?)\s*(?:kwh|kw\.h)\s*(?:total\s*(?:usage|energy|electricity|consumption)|usage)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            try:
                return float(match.group(1).replace(",", ""))
            except ValueError:
                continue
    return None


def _extract_pdf_key_fields(text: str) -> dict:
    normalized_text = _normalize_whitespace(text)
    return {
        "retailer": _extract_retailer(normalized_text),
        "billing_period": _extract_billing_period(normalized_text),
        "total_cost": _extract_total_cost(normalized_text),
        "total_usage_kwh": _extract_total_usage_kwh(normalized_text),
    }
