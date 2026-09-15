import json
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models import Resume, JobDescription, MatchResult
from app.matching import match_resume_to_job
from app.schemas import MatchRequest, MatchResponse, MatchSummary, MatchHistoryResponse

router = APIRouter(prefix="/api/matches", tags=["matches"])


@router.post("", response_model=MatchResponse, status_code=201)
async def run_match(match_req: MatchRequest, db: AsyncSession = Depends(get_db)):
    resume_result = await db.execute(select(Resume).where(Resume.id == match_req.resume_id))
    resume = resume_result.scalar_one_or_none()

    job_result = await db.execute(select(JobDescription).where(JobDescription.id == match_req.job_id))
    job = job_result.scalar_one_or_none()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    if not job:
        raise HTTPException(status_code=404, detail="Job description not found")

    result = match_resume_to_job(resume.raw_text, job.raw_text)

    match = MatchResult(
        resume_id=resume.id,
        job_id=job.id,
        similarity_score=result['similarity_score'],
        matched_keywords=result['matched_keywords'],
        missing_keywords=result['missing_keywords']
    )
    db.add(match)
    await db.commit()
    await db.refresh(match)

    return MatchResponse(
        id=match.id,
        resume_id=match.resume_id,
        job_id=match.job_id,
        similarity_score=match.similarity_score,
        matched_keywords=json.loads(match.matched_keywords),
        missing_keywords=json.loads(match.missing_keywords),
        created_at=match.created_at
    )


@router.get("", response_model=MatchHistoryResponse)
async def list_matches(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    count_result = await db.execute(select(func.count()).select_from(MatchResult))
    total = count_result.scalar()

    offset = (page - 1) * per_page
    result = await db.execute(
        select(MatchResult)
        .order_by(MatchResult.created_at.desc())
        .offset(offset)
        .limit(per_page)
    )
    matches = result.scalars().all()

    pages = (total + per_page - 1) // per_page if total else 0

    return MatchHistoryResponse(
        matches=matches,
        total=total,
        page=page,
        pages=pages
    )


@router.get("/{match_id}", response_model=MatchResponse)
async def get_match(match_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MatchResult).where(MatchResult.id == match_id))
    match = result.scalar_one_or_none()

    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    return MatchResponse(
        id=match.id,
        resume_id=match.resume_id,
        job_id=match.job_id,
        similarity_score=match.similarity_score,
        matched_keywords=json.loads(match.matched_keywords),
        missing_keywords=json.loads(match.missing_keywords),
        created_at=match.created_at
    )