from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Resume(Base):
    __tablename__ = 'resumes'

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    matches: Mapped[list["MatchResult"]] = relationship(back_populates="resume")

    def __repr__(self):
        return f'<Resume {self.id}: {self.filename}>'


class JobDescription(Base):
    __tablename__ = 'job_descriptions'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    matches: Mapped[list["MatchResult"]] = relationship(back_populates="job")

    def __repr__(self):
        return f'<JobDescription {self.id}: {self.title}>'


class MatchResult(Base):
    __tablename__ = 'match_results'

    id: Mapped[int] = mapped_column(primary_key=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey('resumes.id'), nullable=False)
    job_id: Mapped[int] = mapped_column(ForeignKey('job_descriptions.id'), nullable=False)
    similarity_score: Mapped[float] = mapped_column(Float, nullable=False)
    matched_keywords: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    missing_keywords: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    resume: Mapped["Resume"] = relationship(back_populates="matches")
    job: Mapped["JobDescription"] = relationship(back_populates="matches")

    def __repr__(self):
        return f'<MatchResult {self.id}: {self.similarity_score:.2f}>'