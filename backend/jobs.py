from fastapi import APIRouter, HTTPException

from fastapi.params import Query
from sqlmodel import Sequence, select
from typing import Annotated, Sequence
from sqlalchemy.orm import selectinload

from data.database import ExtractedData, Job, SessionDep

router = APIRouter(
    prefix="/jobs"
)

@router.get("")
def read_jobs(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> Sequence[Job]:
    jobs = session.exec(select(Job).offset(offset).limit(limit)).all()
    return jobs

@router.get("/{job_id}")
def read_job(job_id: int, session: SessionDep):
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "id": job.id,
        "file_name": job.file_name,
        "num_pages": job.num_pages,
        "extraction_mode": job.extraction_mode,
        "status": job.status,
        "created_datetime": job.created_datetime,
        "updated_datetime": job.updated_datetime,
        "extracted_data": [
            {
                "id": data.id,
                "page_number": data.page_number,
                "key": data.key,
                "value": data.value,
                "created_datetime": data.created_datetime,
                "updated_datetime": data.updated_datetime,
            }
            for data in job.extracted_data
        ],
    }