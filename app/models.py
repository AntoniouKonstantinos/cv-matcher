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
    skill_gaps: Mapped[list["SkillGapResult"]] = relationship(back_populates="match")

    def __repr__(self):
        return f'<MatchResult {self.id}: {self.similarity_score:.2f}>'


class Skill(Base):
    __tablename__ = 'skills'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self):
        return f'<Skill {self.id}: {self.name} ({self.category})>'


class SkillGapResult(Base):
    __tablename__ = 'skill_gap_results'

    id: Mapped[int] = mapped_column(primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey('match_results.id'), nullable=False)
    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id'), nullable=False)
    present_in_resume: Mapped[bool] = mapped_column(nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)

    match: Mapped["MatchResult"] = relationship(back_populates="skill_gaps")
    skill: Mapped["Skill"] = relationship()

    def __repr__(self):
        return f'<SkillGapResult match={self.match_id} skill={self.skill_id} present={self.present_in_resume}>'