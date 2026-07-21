import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity(resume_text, job_text):
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return float(score)


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
    resume_lower = resume_text.lower()

    matched = []
    missing = []

    for kw in job_keywords:
        if kw.lower() in resume_lower:
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