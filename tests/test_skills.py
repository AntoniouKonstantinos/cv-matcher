import pytest
from app.skills import analyze_skills_gap


class FakeSkill:
    def __init__(self, name, category):
        self.name = name
        self.category = category


def test_analyze_skills_gap_empty_list_returns_empty():
    result = analyze_skills_gap("some resume", "some job", [])
    assert result == []


def test_analyze_skills_gap_filters_irrelevant_skills():
    resume = "Experienced chef specializing in French cuisine"
    job = "Professional chef role, French cuisine restaurant, fine dining experience"
    skills = [
        FakeSkill("Python", "language"),
        FakeSkill("Kubernetes", "tool"),
    ]

    result = analyze_skills_gap(resume, job, skills)

    assert result == []


def test_analyze_skills_gap_detects_present_skill():
    resume = "Experienced Python developer with strong Flask background"
    job = "Looking for a Python developer with Flask experience"
    skills = [FakeSkill("Python", "language")]

    result = analyze_skills_gap(resume, job, skills)

    assert len(result) == 1
    assert result[0]['skill_name'] == "Python"
    assert result[0]['present_in_resume'] is True


def test_analyze_skills_gap_detects_missing_skill():
    resume = "Marketing specialist with content writing background"
    job = "Python developer role requiring Docker containerization experience"
    skills = [
        FakeSkill("Python", "language"),
        FakeSkill("Docker", "tool"),
    ]

    result = analyze_skills_gap(resume, job, skills)

    skill_names = [r['skill_name'] for r in result]
    assert "Docker" in skill_names

    docker_result = next(r for r in result if r['skill_name'] == "Docker")
    assert docker_result['present_in_resume'] is False


def test_analyze_skills_gap_includes_category():
    resume = "Python developer with Flask experience"
    job = "Looking for a Python developer with Flask experience"
    skills = [FakeSkill("Python", "language")]

    result = analyze_skills_gap(resume, job, skills)

    assert result[0]['category'] == "language"


def test_analyze_skills_gap_confidence_score_is_float_between_0_and_1():
    resume = "Python developer with Flask experience"
    job = "Looking for a Python developer with Flask experience"
    skills = [FakeSkill("Python", "language")]

    result = analyze_skills_gap(resume, job, skills)

    score = result[0]['confidence_score']
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0


def test_analyze_skills_gap_sorted_by_confidence_descending():
    resume = "Senior Python developer with extensive Flask and Docker experience"
    job = "Python developer role, Flask and Docker experience required"
    skills = [
        FakeSkill("Python", "language"),
        FakeSkill("Flask", "framework"),
        FakeSkill("Docker", "tool"),
    ]

    result = analyze_skills_gap(resume, job, skills)

    scores = [r['confidence_score'] for r in result]
    assert scores == sorted(scores, reverse=True)