document.addEventListener('DOMContentLoaded', () => {

    let currentResumeId = null;
    let currentJobId = null;

    const resumeForm = document.getElementById('resume-form');
    const resumeFileInput = document.getElementById('resume-file');
    const resumeStatus = document.getElementById('resume-status');

    const jobForm = document.getElementById('job-form');
    const jobTitleInput = document.getElementById('job-title');
    const jobTextInput = document.getElementById('job-text');
    const jobStatus = document.getElementById('job-status');

    const matchBtn = document.getElementById('match-btn');
    const matchResult = document.getElementById('match-result');
    const scoreDisplay = document.getElementById('score-display');
    const matchedList = document.getElementById('matched-keywords');
    const missingList = document.getElementById('missing-keywords');

    const historyBody = document.getElementById('history-body');

    function showStatus(el, message, type) {
        el.textContent = message;
        el.className = 'status ' + type;
    }

    function checkMatchReady() {
        matchBtn.disabled = !(currentResumeId && currentJobId);
    }

    resumeForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const file = resumeFileInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/resumes', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                showStatus(resumeStatus, data.error || 'Upload failed', 'error');
                return;
            }

            currentResumeId = data.id;
            showStatus(resumeStatus, `Uploaded: ${data.filename}`, 'success');
            checkMatchReady();

        } catch (err) {
            showStatus(resumeStatus, 'Network error, please try again', 'error');
        }
    });

    jobForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const text = jobTextInput.value.trim();
        if (!text) return;

        try {
            const response = await fetch('/api/jobs', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title: jobTitleInput.value.trim() || null,
                    text: text
                })
            });

            const data = await response.json();

            if (!response.ok) {
                showStatus(jobStatus, data.error || 'Failed to save job description', 'error');
                return;
            }

            currentJobId = data.id;
            showStatus(jobStatus, 'Job description saved', 'success');
            checkMatchReady();

        } catch (err) {
            showStatus(jobStatus, 'Network error, please try again', 'error');
        }
    });

    matchBtn.addEventListener('click', async () => {
        if (!currentResumeId || !currentJobId) return;

        matchBtn.disabled = true;
        matchBtn.textContent = 'Matching...';

        try {
            const response = await fetch('/api/match', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    resume_id: currentResumeId,
                    job_id: currentJobId
                })
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.error || 'Matching failed');
                return;
            }

            displayMatchResult(data);
            loadHistory();

        } catch (err) {
            alert('Network error, please try again');
        } finally {
            matchBtn.disabled = false;
            matchBtn.textContent = 'Run Match';
        }
    });

    function displayMatchResult(data) {
        matchResult.classList.remove('hidden');

        const percentage = Math.round(data.similarity_score * 100);
        scoreDisplay.textContent = `${percentage}%`;

        matchedList.innerHTML = '';
        data.matched_keywords.forEach(kw => {
            const li = document.createElement('li');
            li.textContent = kw;
            matchedList.appendChild(li);
        });

        missingList.innerHTML = '';
        data.missing_keywords.forEach(kw => {
            const li = document.createElement('li');
            li.textContent = kw;
            missingList.appendChild(li);
        });
    }

    async function loadHistory() {
        try {
            const response = await fetch('/api/matches?per_page=10');
            const data = await response.json();

            historyBody.innerHTML = '';

            data.matches.forEach(m => {
                const row = document.createElement('tr');
                const percentage = Math.round(m.similarity_score * 100);
                const date = new Date(m.created_at).toLocaleDateString();

                row.innerHTML = `
                    <td>${m.id}</td>
                    <td>${percentage}%</td>
                    <td>${date}</td>
                `;
                historyBody.appendChild(row);
            });

        } catch (err) {
            console.error('Failed to load match history', err);
        }
    }

    loadHistory();

});