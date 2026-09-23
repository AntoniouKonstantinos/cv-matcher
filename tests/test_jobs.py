import pytest


@pytest.mark.asyncio
async def test_submit_job_success(client):
    payload = {"title": "Python Developer", "text": "Looking for a Flask developer"}

    response = await client.post("/api/jobs", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Python Developer"
    assert "id" in data


@pytest.mark.asyncio
async def test_submit_job_without_title(client):
    payload = {"text": "Looking for a backend developer"}

    response = await client.post("/api/jobs", json=payload)

    assert response.status_code == 201
    assert response.json()["title"] is None


@pytest.mark.asyncio
async def test_submit_job_missing_text(client):
    payload = {"title": "Some Job"}

    response = await client.post("/api/jobs", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_submit_job_empty_text(client):
    payload = {"text": "   "}

    response = await client.post("/api/jobs", json=payload)

    assert response.status_code == 400