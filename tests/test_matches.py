import pytest


async def _create_resume(client, text="Python developer with Flask and SQL experience"):
    import io
    files = {"file": ("resume.txt", io.BytesIO(text.encode()), "text/plain")}
    response = await client.post("/api/resumes", files=files)
    return response.json()["id"]


async def _create_job(client, text="Looking for a Python developer with Flask experience"):
    response = await client.post("/api/jobs", json={"text": text})
    return response.json()["id"]


@pytest.mark.asyncio
async def test_run_match_success(client):
    resume_id = await _create_resume(client)
    job_id = await _create_job(client)

    response = await client.post("/api/matches", json={"resume_id": resume_id, "job_id": job_id})

    assert response.status_code == 201
    data = response.json()
    assert "similarity_score" in data
    assert isinstance(data["matched_keywords"], list)
    assert isinstance(data["missing_keywords"], list)


@pytest.mark.asyncio
async def test_run_match_resume_not_found(client):
    job_id = await _create_job(client)

    response = await client.post("/api/matches", json={"resume_id": 999, "job_id": job_id})

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_matches_pagination(client):
    resume_id = await _create_resume(client)
    job_id = await _create_job(client)

    for _ in range(3):
        await client.post("/api/matches", json={"resume_id": resume_id, "job_id": job_id})

    response = await client.get("/api/matches?page=1&per_page=2")

    assert response.status_code == 200
    data = response.json()
    assert len(data["matches"]) == 2
    assert data["total"] == 3
    assert data["pages"] == 2


@pytest.mark.asyncio
async def test_list_matches_invalid_page(client):
    response = await client.get("/api/matches?page=0")

    assert response.status_code == 422