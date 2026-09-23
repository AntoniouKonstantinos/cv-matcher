import io
import pytest


@pytest.mark.asyncio
async def test_upload_resume_success(client):
    file_content = b"Python developer with Flask and SQL experience"
    files = {"file": ("resume.txt", io.BytesIO(file_content), "text/plain")}

    response = await client.post("/api/resumes", files=files)

    assert response.status_code == 201
    data = response.json()
    assert data["filename"] == "resume.txt"
    assert "id" in data


@pytest.mark.asyncio
async def test_upload_resume_invalid_extension(client):
    file_content = b"some content"
    files = {"file": ("resume.exe", io.BytesIO(file_content), "application/octet-stream")}

    response = await client.post("/api/resumes", files=files)

    assert response.status_code == 400
    assert "not allowed" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_resume_not_found(client):
    response = await client.get("/api/resumes/999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_resume_after_upload(client):
    file_content = b"Experienced backend developer"
    files = {"file": ("cv.txt", io.BytesIO(file_content), "text/plain")}

    upload_response = await client.post("/api/resumes", files=files)
    resume_id = upload_response.json()["id"]

    get_response = await client.get(f"/api/resumes/{resume_id}")

    assert get_response.status_code == 200
    data = get_response.json()
    assert data["raw_text"] == "Experienced backend developer"