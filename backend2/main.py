from fastapi import FastAPI, HTTPException, UploadFile, File

import simple_extraction
import advanced_extraction

app = FastAPI()

app.include_router(simple_extraction.router)
app.include_router(advanced_extraction.router)

@app.get("/")
def main():
    return {"message": "Hello World"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Optional: Validate file extension or MIME type
    if file.content_type not in ["image/jpeg", "image/png", "application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type.")
        
    return {"filename": file.filename, "content_type": file.content_type}