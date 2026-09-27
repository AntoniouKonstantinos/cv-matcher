from sentence_transformers import util
from app.matching import get_model, MATCH_THRESHOLD

JOB_RELEVANCE_THRESHOLD = 0.35


def analyze_skills_gap(resume_text, job_text, skills):
    if not skills:
        return []

    model = get_model()

    job_embedding = model.encode(job_text, convert_to_tensor=True)
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)

    skill_names = [skill.name for skill in skills]
    skill_embeddings = model.encode(skill_names, convert_to_tensor=True)

    job_similarities = util.cos_sim(skill_embeddings, job_embedding).squeeze(1)
    resume_similarities = util.cos_sim(skill_embeddings, resume_embedding).squeeze(1)

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