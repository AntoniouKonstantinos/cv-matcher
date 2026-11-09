import json
from functools import lru_cache
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS

from app.chunking import split_into_chunks

MODEL_NAME = "all-MiniLM-L6-v2"
MATCH_THRESHOLD = 0.30

GENERIC_JOB_WORDS = {
    'job', 'role', 'position', 'candidate', 'candidates', 'company',
    'team', 'teams', 'work', 'working', 'works', 'experience', 'experienced',
    'strong', 'good', 'great', 'excellent', 'ability', 'skills', 'skill',
    'knowledge', 'understanding', 'responsibilities', 'requirements',
    'required', 'preferred', 'plus', 'looking', 'join', 'based', 'build',
    'building', 'built', 'designing', 'real', 'time', 'fast', 'help', 'new',
    'including', 'ideal', 'must', 'will', 'etc', 'internal', 'operational',
    'product', 'business', 'environment', 'opportunity', 'across', 'within',
    'using', 'use', 'highly', 'high', 'impact', 'full', 'description',
    'years', 'year',
}
KEYWORD_STOP_WORDS = list(ENGLISH_STOP_WORDS | GENERIC_JOB_WORDS)


@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer(MODEL_NAME)


def compute_similarity(resume_text, job_text):
    resume_chunks = split_into_chunks(resume_text)
    job_chunks = split_into_chunks(job_text)

    if not resume_chunks or not job_chunks:
        return 0.0

    model = get_model()
    resume_embeddings = model.encode(resume_chunks, convert_to_tensor=True)
    job_embeddings = model.encode(job_chunks, convert_to_tensor=True)

    similarities = util.cos_sim(job_embeddings, resume_embeddings)
    best_match_per_job_chunk = similarities.max(dim=1).values

    return float(best_match_per_job_chunk.mean().item())


def extract_keywords(job_text, top_n=20):
    vectorizer = TfidfVectorizer(stop_words=KEYWORD_STOP_WORDS, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform([job_text])

    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

    keyword_scores = list(zip(feature_names, scores))
    keyword_scores.sort(key=lambda x: x[1], reverse=True)

    return [kw for kw, score in keyword_scores[:top_n]]


def compare_keywords(resume_text, job_text, top_n=20):
    job_keywords = extract_keywords(job_text, top_n=top_n)

    if not job_keywords:
        return [], []

    resume_chunks = split_into_chunks(resume_text)

    if not resume_chunks:
        return [], job_keywords

    model = get_model()
    chunk_embeddings = model.encode(resume_chunks, convert_to_tensor=True)
    keyword_embeddings = model.encode(job_keywords, convert_to_tensor=True)

    best_match_per_keyword = util.cos_sim(keyword_embeddings, chunk_embeddings).max(dim=1).values

    matched = []
    missing = []

    for kw, sim in zip(job_keywords, best_match_per_keyword):
        if sim.item() >= MATCH_THRESHOLD:
            matched.append(kw)
        else:
            missing.append(kw)

    return matched, missing


def match_resume_to_job(resume_text, job_text):
    score = compute_similarity(resume_text, job_text)
    matched, missing = compare_keywords(resume_text, job_text)

    return {
        'similarity_score': score,
        'matched_keywords': json.dumps(matched),
        'missing_keywords': json.dumps(missing)
    }