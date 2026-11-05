import re
from functools import lru_cache
from sentence_transformers import util

from app.chunking import split_into_chunks
from app.matching import get_model

SEMANTIC_JOB_THRESHOLD = 0.45
SEMANTIC_RESUME_THRESHOLD = 0.40
EXPLICIT_CONFIDENCE = 1.0

SKILL_ALIASES = {
    'JavaScript': ['ecmascript'],
    'C#': ['c sharp', 'csharp'],
    'C++': ['cpp'],
    'HTML': ['html5'],
    'CSS': ['css3'],
    'React': ['reactjs', 'react.js'],
    'Vue.js': ['vuejs', 'vue'],
    'Node.js': ['nodejs', 'node js'],
    'Express.js': ['expressjs', 'express js'],
    'Next.js': ['nextjs', 'next js'],
    'Spring Boot': ['springboot'],
    'ASP.NET': ['aspnet', 'asp net', '.net core'],
    'Tailwind CSS': ['tailwind'],
    'scikit-learn': ['sklearn', 'scikit learn'],
    'PostgreSQL': ['postgres'],
    'MongoDB': ['mongo'],
    'Microsoft SQL Server': ['mssql', 'sql server', 'ms sql'],
    'Oracle Database': ['oracle db'],
    'Elasticsearch': ['elastic search'],
    'Git': ['github', 'gitlab'],
    'Kubernetes': ['k8s'],
    'AWS': ['amazon web services'],
    'Microsoft Azure': ['azure'],
    'Google Cloud Platform': ['gcp', 'google cloud'],
    'GitHub Actions': ['github action'],
    'Jupyter Notebook': ['jupyter'],
    'Power BI': ['powerbi'],
    'REST API': ['restful', 'rest apis', 'restful api', 'restful apis'],
    'CI/CD': ['ci cd', 'cicd', 'continuous integration', 'continuous delivery', 'continuous deployment'],
    'Test-driven development': ['tdd', 'test driven'],
    'Unit testing': ['unit tests'],
    'Object-oriented programming': ['oop', 'object oriented'],
    'Data structures and algorithms': ['data structures', 'algorithms'],
    'Version control': ['source control'],
    'Code review': ['code reviews', 'peer review'],
    'Microservices': ['microservice'],
    'Data analysis': ['data analytics'],
    'Responsive design': ['responsive'],
    'Database design': ['database schema', 'schema design'],
    'Authentication and authorization': ['authentication', 'authorization'],
    'Teamwork': ['team player', 'team work'],
    'Collaboration': ['collaborate', 'collaborated', 'collaborating', 'collaborative'],
    'Leadership': ['team lead', 'led a team', 'leading a team'],
    'Problem solving': ['problem-solving'],
    'Analytical thinking': ['analytical skills'],
    'Attention to detail': ['detail-oriented', 'detail oriented'],
    'Adaptability': ['adaptable'],
    'Creativity': ['creative'],
    'Mentoring': ['mentor', 'mentored', 'mentorship'],
    'Stakeholder management': ['stakeholders'],
    'Customer service': ['customer support'],
}


@lru_cache(maxsize=None)
def _compile_term(term):
    return re.compile(
        r'(?<![A-Za-z0-9])' + re.escape(term) + r'(?![A-Za-z0-9])',
        re.IGNORECASE
    )


def mentions_skill(text, skill_name):
    terms = [skill_name] + SKILL_ALIASES.get(skill_name, [])
    return any(_compile_term(term).search(text) for term in terms)


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
        job_sim = job_sim.item()
        resume_sim = resume_sim.item()

        if not mentions_skill(job_text, skill.name) and job_sim < SEMANTIC_JOB_THRESHOLD:
            continue

        if mentions_skill(resume_text, skill.name):
            present = True
            confidence = EXPLICIT_CONFIDENCE
        else:
            present = resume_sim >= SEMANTIC_RESUME_THRESHOLD
            confidence = resume_sim

        results.append({
            'skill_name': skill.name,
            'category': skill.category,
            'present_in_resume': present,
            'confidence_score': round(confidence, 4)
        })

    results.sort(key=lambda r: r['confidence_score'], reverse=True)

    return results