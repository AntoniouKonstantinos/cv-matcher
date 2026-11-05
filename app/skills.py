from sentence_transformers import util

from app.chunking import split_into_chunks
from app.matching import get_model, MATCH_THRESHOLD

JOB_RELEVANCE_THRESHOLD = 0.35


def analyze_skills_gap(resume_text, job_text, skills):
    if not skills:
        return []

    resume_chunks = split_into_chunks(resume_text)
    job_chunks = split_into_chunks(job_text)

    if not resume_chunks or not job_chunks:
        return []

    model = get_model()

    resume_embeddings = model.encode(resume_chunks, convert_to_tensor=True)
    job_embeddings = model.encode(job_chunks, convert_to_tensor=True)

    skill_names = [skill.name for skill in skills]
    skill_embeddings = model.encode(skill_names, convert_to_tensor=True)

    job_similarities = util.cos_sim(skill_embeddings, job_embeddings).max(dim=1).values
    resume_similarities = util.cos_sim(skill_embeddings, resume_embeddings).max(dim=1).values

    results = []

    for skill, job_sim, resume_sim in zip(skills, job_similarities, resume_similarities):
        if job_sim.item() < JOB_RELEVANCE_THRESHOLD:
            continue

        present = resume_sim.item() >= MATCH_THRESHOLD

        results.append({
            'skill_name': skill.name,
            'category': skill.category,
            'present_in_resume': present,
            'confidence_score': round(resume_sim.item(), 4)
        })

    results.sort(key=lambda r: r['confidence_score'], reverse=True)

    return results