import json
import pytest
from app.matching import compute_similarity, extract_keywords, compare_keywords, match_resume_to_job


def test_compute_similarity_identical_texts():
    text = "Python developer with Flask and SQL experience"
    score = compute_similarity(text, text)

    assert score == pytest.approx(1.0, abs=0.01)


def test_compute_similarity_unrelated_texts():
    resume = "Professional chef specializing in French cuisine"
    job = "Senior Java backend engineer with Kubernetes experience"

    score = compute_similarity(resume, job)

    assert score < 0.2


def test_compute_similarity_returns_float():
    score = compute_similarity("python developer", "python engineer")
    assert isinstance(score, float)


def test_extract_keywords_returns_list():
    job_text = "We need a Python developer with Flask and SQL experience"
    keywords = extract_keywords(job_text, top_n=5)

    assert isinstance(keywords, list)
    assert len(keywords) <= 5


def test_compare_keywords_finds_matches():
    resume = "Experienced Python developer skilled in Flask and PostgreSQL"
    job = "Looking for a Python developer familiar with Flask"

    matched, missing = compare_keywords(resume, job)

    assert any('python' in kw.lower() for kw in matched)


def test_compare_keywords_finds_missing():
    resume = "Marketing specialist with content writing background"
    job = "Python developer with Docker and Kubernetes experience"

    matched, missing = compare_keywords(resume, job)

    assert len(missing) > 0


def test_match_resume_to_job_structure():
    resume = "Python developer with Flask experience"
    job = "Looking for a Python developer"

    result = match_resume_to_job(resume, job)

    assert 'similarity_score' in result
    assert 'matched_keywords' in result
    assert 'missing_keywords' in result

    assert isinstance(result['similarity_score'], float)
    assert isinstance(json.loads(result['matched_keywords']), list)
    assert isinstance(json.loads(result['missing_keywords']), list)