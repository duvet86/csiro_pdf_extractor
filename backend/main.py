from contextlib import asynccontextmanager
import select

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.params import Query
from sqlmodel import Sequence, select
from typing import Annotated, Sequence

from data.database import Job, SessionDep, create_db_and_tables
import simple_extraction
import advanced_extraction

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

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

@app.get("/jobs")
def read_jobs(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> Sequence[Job]:
    jobs = session.exec(select(Job).offset(offset).limit(limit)).all()
    return jobs