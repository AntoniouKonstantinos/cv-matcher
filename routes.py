import os
import json
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from app import db
from app.models import Resume, JobDescription, MatchResult
from app.extraction import extract_text, allowed_file
from app.matching import match_resume_to_job


main = Blueprint('main', __name__)


@main.route('/api/resumes', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    filename = secure_filename(file.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    try:
        raw_text = extract_text(filepath)
    except Exception as e:
        return jsonify({'error': f'Failed to extract text: {str(e)}'}), 500
    finally:
        os.remove(filepath)

    if not raw_text.strip():
        return jsonify({'error': 'No text could be extracted from file'}), 400

    resume = Resume(filename=filename, raw_text=raw_text)
    db.session.add(resume)
    db.session.commit()

    return jsonify({
        'id': resume.id,
        'filename': resume.filename,
        'uploaded_at': resume.uploaded_at.isoformat()
    }), 201


@main.route('/api/jobs', methods=['POST'])
def submit_job():
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Missing job description text'}), 400

    raw_text = data['text'].strip()
    if not raw_text:
        return jsonify({'error': 'Job description text cannot be empty'}), 400

    title = data.get('title')

    job = JobDescription(title=title, raw_text=raw_text)
    db.session.add(job)
    db.session.commit()

    return jsonify({
        'id': job.id,
        'title': job.title,
        'created_at': job.created_at.isoformat()
    }), 201


@main.route('/api/match', methods=['POST'])
def run_match():
    data = request.get_json()

    if not data or 'resume_id' not in data or 'job_id' not in data:
        return jsonify({'error': 'resume_id and job_id are required'}), 400

    resume = Resume.query.get(data['resume_id'])
    job = JobDescription.query.get(data['job_id'])

    if not resume:
        return jsonify({'error': 'Resume not found'}), 404
    if not job:
        return jsonify({'error': 'Job description not found'}), 404

    result = match_resume_to_job(resume.raw_text, job.raw_text)

    match = MatchResult(
        resume_id=resume.id,
        job_id=job.id,
        similarity_score=result['similarity_score'],
        matched_keywords=result['matched_keywords'],
        missing_keywords=result['missing_keywords']
    )
    db.session.add(match)
    db.session.commit()

    return jsonify({
        'id': match.id,
        'resume_id': match.resume_id,
        'job_id': match.job_id,
        'similarity_score': match.similarity_score,
        'matched_keywords': json.loads(match.matched_keywords),
        'missing_keywords': json.loads(match.missing_keywords),
        'created_at': match.created_at.isoformat()
    }), 201


@main.route('/api/matches', methods=['GET'])
def list_matches():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    pagination = MatchResult.query.order_by(
        MatchResult.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    results = [{
        'id': m.id,
        'resume_id': m.resume_id,
        'job_id': m.job_id,
        'similarity_score': m.similarity_score,
        'created_at': m.created_at.isoformat()
    } for m in pagination.items]

    return jsonify({
        'matches': results,
        'total': pagination.total,
        'page': page,
        'pages': pagination.pages
    }), 200


@main.route('/api/matches/<int:match_id>', methods=['GET'])
def get_match(match_id):
    match = MatchResult.query.get(match_id)

    if not match:
        return jsonify({'error': 'Match not found'}), 404

    return jsonify({
        'id': match.id,
        'resume_id': match.resume_id,
        'job_id': match.job_id,
        'similarity_score': match.similarity_score,
        'matched_keywords': json.loads(match.matched_keywords),
        'missing_keywords': json.loads(match.missing_keywords),
        'created_at': match.created_at.isoformat()
    }), 200


@main.route('/api/resumes/<int:resume_id>', methods=['GET'])
def get_resume(resume_id):
    resume = Resume.query.get(resume_id)

    if not resume:
        return jsonify({'error': 'Resume not found'}), 404

    return jsonify({
        'id': resume.id,
        'filename': resume.filename,
        'raw_text': resume.raw_text,
        'uploaded_at': resume.uploaded_at.isoformat()
    }), 200


@main.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = JobDescription.query.get(job_id)

    if not job:
        return jsonify({'error': 'Job description not found'}), 404

    return jsonify({
        'id': job.id,
        'title': job.title,
        'raw_text': job.raw_text,
        'created_at': job.created_at.isoformat()
    }), 200