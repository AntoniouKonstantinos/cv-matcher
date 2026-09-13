import os
import json
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import Resume
from app.extraction import extract_text, allowed_file
from app.schemas import ResumeResponse, ResumeDetail

router = APIRouter(prefix="/api/resumes", tags=["resumes"])

UPLOAD_FOLDER = os.path.join(
    os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
    'uploads'
)


@router.post("", response_model=ResumeResponse, status_code=201)
async def upload_resume(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    contents = await file.read()
    with open(filepath, 'wb') as f:
        f.write(contents)

    try:
        raw_text = extract_text(filepath)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")
    finally:
        os.remove(filepath)

    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="No text could be extracted from file")

    resume = Resume(filename=file.filename, raw_text=raw_text)
    db.add(resume)
    await db.commit()
    await db.refresh(resume)

    return resume


@router.get("/{resume_id}", response_model=ResumeDetail)
async def get_resume(resume_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    return resume