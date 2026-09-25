import json
from functools import lru_cache
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer

MODEL_NAME = "all-MiniLM-L6-v2"
MATCH_THRESHOLD = 0.45


@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer(MODEL_NAME)


def compute_similarity(resume_text, job_text):
    model = get_model()
    embeddings = model.encode([resume_text, job_text], convert_to_tensor=True)
    score = util.cos_sim(embeddings[0], embeddings[1])
    return float(score.item())


def extract_keywords(job_text, top_n=20):
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
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

    model = get_model()
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    keyword_embeddings = model.encode(job_keywords, convert_to_tensor=True)

    similarities = util.cos_sim(keyword_embeddings, resume_embedding).squeeze(1)

    matched = []
    missing = []

    for kw, sim in zip(job_keywords, similarities):
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