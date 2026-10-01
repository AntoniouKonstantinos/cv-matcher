const API_BASE_URL = "http://127.0.0.1:8000";

export async function uploadResume(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/api/resumes`, {
        method: "POST",
        body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Upload failed");
    }

    return data;
}

export async function submitJob(title, text) {
    const response = await fetch(`${API_BASE_URL}/api/jobs`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: title || null, text }),
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Failed to save job description");
    }

    return data;
}

export async function runMatch(resumeId, jobId) {
    const response = await fetch(`${API_BASE_URL}/api/matches`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_id: resumeId, job_id: jobId }),
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Matching failed");
    }

    return data;
}

export async function getSkillsGap(matchId) {
    const response = await fetch(`${API_BASE_URL}/api/matches/${matchId}/skills-gap`);

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Failed to load skills gap");
    }

    return data;
}

export async function getMatchHistory(page = 1, perPage = 10) {
    const response = await fetch(`${API_BASE_URL}/api/matches?page=${page}&per_page=${perPage}`);

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Failed to load match history");
    }

    return data;
}