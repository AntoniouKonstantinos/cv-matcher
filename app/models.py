from datetime import datetime
from app import db


class Resume(db.Model):
    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    raw_text = db.Column(db.Text, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    matches = db.relationship('MatchResult', backref='resume', lazy=True)

    def __repr__(self):
        return f'<Resume {self.id}: {self.filename}>'


class JobDescription(db.Model):
    __tablename__ = 'job_descriptions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    raw_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    matches = db.relationship('MatchResult', backref='job', lazy=True)

    def __repr__(self):
        return f'<JobDescription {self.id}: {self.title}>'


class MatchResult(db.Model):
    __tablename__ = 'match_results'

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_descriptions.id'), nullable=False)
    similarity_score = db.Column(db.Float, nullable=False)
    matched_keywords = db.Column(db.Text, nullable=True)   # JSON string
    missing_keywords = db.Column(db.Text, nullable=True)   # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<MatchResult {self.id}: {self.similarity_score:.2f}>'