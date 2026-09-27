from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ResumeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    uploaded_at: datetime


class ResumeDetail(ResumeResponse):
    raw_text: str


class JobCreate(BaseModel):
    title: Optional[str] = None
    text: str


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: Optional[str]
    created_at: datetime


class JobDetail(JobResponse):
    raw_text: str


class MatchRequest(BaseModel):
    resume_id: int
    job_id: int


class MatchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    resume_id: int
    job_id: int
    similarity_score: float
    matched_keywords: list[str]
    missing_keywords: list[str]
    created_at: datetime


class MatchSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    resume_id: int
    job_id: int
    similarity_score: float
    created_at: datetime


class MatchHistoryResponse(BaseModel):
    matches: list[MatchSummary]
    total: int
    page: int
    pages: int


class ErrorResponse(BaseModel):
    error: str


class SkillGapItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    skill_name: str
    category: str
    present_in_resume: bool
    confidence_score: float


class SkillsGapResponse(BaseModel):
    match_id: int
    skills: list[SkillGapItem]