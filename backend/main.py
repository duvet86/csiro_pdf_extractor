# # import io
# # import re
# from fastapi import FastAPI, UploadFile, File, HTTPException
# # import pdfplumber
# from pypdf import PdfReader

from typing import Annotated
from fastapi import FastAPI, File, UploadFile

# Initialize the core FastAPI instance
app = FastAPI(title="My First FastAPI App")

@app.post("/upload/")
async def upload_file(file: Annotated[UploadFile, File()]):
    # Read metadata or content
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size
    }

# def _normalize_whitespace(text: str) -> str:
#     return re.sub(r"\s+", " ", text).strip()


# def _extract_retailer(text: str) -> str | None:
#     label_patterns = [
#         r"(?:retailer|energy\s+retailer|issued\s+by|sold\s+by)\s*[:\-]\s*([A-Za-z][A-Za-z0-9&.,'()\-\s]{2,80})",
#         r"(?:retailer|energy\s+retailer)\s+([A-Za-z][A-Za-z0-9&.,'()\-\s]{2,80})",
#     ]
#     for pattern in label_patterns:
#         match = re.search(pattern, text, flags=re.IGNORECASE)
#         if match:
#             return _normalize_whitespace(match.group(1))
#     return None


# def _extract_billing_period(text: str) -> str | None:
#     label_patterns = [
#         r"(?:billing|bill)\s*(?:period|cycle)\s*[:\-]\s*([^\n]{5,80})",
#         r"(?:for\s+the\s+period)\s*[:\-]?\s*([^\n]{5,80})",
#     ]
#     for pattern in label_patterns:
#         match = re.search(pattern, text, flags=re.IGNORECASE)
#         if match:
#             return _normalize_whitespace(match.group(1))

#     range_patterns = [
#         r"(\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b\s*(?:to|-|–|—)\s*\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b)",
#         r"(\b\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4}\b\s*(?:to|-|–|—)\s*\b\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4}\b)",
#     ]
#     for pattern in range_patterns:
#         match = re.search(pattern, text, flags=re.IGNORECASE)
#         if match:
#             return _normalize_whitespace(match.group(1))
#     return None


# def _extract_total_cost(text: str) -> float | None:
#     patterns = [
#         r"(?:total\s*(?:amount\s*due|cost|charges?|bill)|amount\s*due)\s*[:\-]?\s*\$?\s*([0-9][0-9,]*(?:\.[0-9]{2})?)",
#         r"\$\s*([0-9][0-9,]*(?:\.[0-9]{2})?)\s*(?:total\s*(?:amount\s*due|cost|charges?|bill)|amount\s*due)",
#     ]
#     for pattern in patterns:
#         match = re.search(pattern, text, flags=re.IGNORECASE)
#         if match:
#             try:
#                 return float(match.group(1).replace(",", ""))
#             except ValueError:
#                 continue
#     return None


# def _extract_total_usage_kwh(text: str) -> float | None:
#     patterns = [
#         r"(?:total\s*(?:usage|energy|electricity|consumption)|usage)\s*(?:\(?(?:kwh|kw\.h)\)?)?\s*[:\-]?\s*([0-9][0-9,]*(?:\.[0-9]+)?)\s*(?:kwh|kw\.h)?",
#         r"([0-9][0-9,]*(?:\.[0-9]+)?)\s*(?:kwh|kw\.h)\s*(?:total\s*(?:usage|energy|electricity|consumption)|usage)",
#     ]
#     for pattern in patterns:
#         match = re.search(pattern, text, flags=re.IGNORECASE)
#         if match:
#             try:
#                 return float(match.group(1).replace(",", ""))
#             except ValueError:
#                 continue
#     return None


# def _extract_pdf_key_fields(text: str) -> dict:
#     normalized_text = _normalize_whitespace(text)
#     return {
#         "retailer": _extract_retailer(normalized_text),
#         "billing_period": _extract_billing_period(normalized_text),
#         "total_cost": _extract_total_cost(normalized_text),
#         "total_usage_kwh": _extract_total_usage_kwh(normalized_text),
#     }

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI application!"}

# @app.post("/extract-pdf/")
# async def extract_pdf_text(file: UploadFile = File(...)):
#     # Validate that the uploaded file is actually a PDF
#     if file.content_type != "application/pdf":
#         raise HTTPException(
#             status_code=400, 
#             detail="Invalid file type. Please upload a PDF file."
#         )
    
#     try:
#         # Read the file contents into memory as bytes
#         pdf_bytes = await file.read()
        
#         # Convert bytes to a stream that pypdf can read
#         pdf_stream = io.BytesIO(pdf_bytes)
#         reader = PdfReader(pdf_stream)
        
#         # Extract text from each page
#         extracted_text = {}
#         for page_num, page in enumerate(reader.pages, start=1):
#             text = page.extract_text()
#             extracted_text[f"page_{page_num}"] = text or "[No readable text found]"
            
#         return {
#             "filename": file.filename,
#             "total_pages": len(reader.pages),
#             "content": extracted_text
#         }
        
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, 
#             detail=f"An error occurred while processing the PDF: {str(e)}"
#         )


# @app.post("/extract-pdf-fields/")
# async def extract_pdf_fields(file: UploadFile = File(...)):
#     # Accept standard PDF MIME type and fallback to extension check for some clients.
#     is_pdf_mime = file.content_type == "application/pdf"
#     is_pdf_filename = bool(file.filename and file.filename.lower().endswith(".pdf"))
#     if not (is_pdf_mime or is_pdf_filename):
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid file type. Please upload a PDF file.",
#         )

#     try:
#         pdf_bytes = await file.read()
#         with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
#             page_text = [page.extract_text() or "" for page in pdf.pages]
#             total_pages = len(pdf.pages)

#         full_text = "\n".join(page_text)
#         fields = _extract_pdf_key_fields(full_text)

#         return {
#             "filename": file.filename,
#             "total_pages": total_pages,
#             "extracted_fields": fields,
#         }

#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"An error occurred while processing the PDF: {str(e)}",
#         )