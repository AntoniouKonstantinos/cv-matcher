from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import JobDescription
from app.schemas import JobCreate, JobResponse, JobDetail

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.post("", response_model=JobResponse, status_code=201)
async def submit_job(job: JobCreate, db: AsyncSession = Depends(get_db)):
    raw_text = job.text.strip()
    if not raw_text:
        raise HTTPException(status_code=400, detail="Job description text cannot be empty")

    job_obj = JobDescription(title=job.title, raw_text=raw_text)
    db.add(job_obj)
    await db.commit()
    await db.refresh(job_obj)

    return job_obj


@router.get("/{job_id}", response_model=JobDetail)
async def get_job(job_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JobDescription).where(JobDescription.id == job_id))
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Job description not found")

    return job