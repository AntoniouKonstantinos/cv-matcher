import { useState } from "react";
import { submitJob } from "../api";

function JobDescriptionForm({ onJobSaved }) {
    const [title, setTitle] = useState("");
    const [text, setText] = useState("");
    const [status, setStatus] = useState(null);
    const [statusType, setStatusType] = useState(null);

    async function handleSubmit(e) {
        e.preventDefault();

        const trimmedText = text.trim();
        if (!trimmedText) return;

        try {
            const data = await submitJob(title.trim(), trimmedText);
            setStatus("Job description saved");
            setStatusType("success");
            onJobSaved(data.id);
        } catch (err) {
            setStatus(err.message);
            setStatusType("error");
        }
    }

    return (
        <section>
            <h2>2. Job Description</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Job title (optional)"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />
                <textarea
                    rows={8}
                    placeholder="Paste the job description here..."
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    required
                />
                <button type="submit">Save Job Description</button>
            </form>
            {status && <p className={`status ${statusType}`}>{status}</p>}
        </section>
    );
}

export default JobDescriptionForm;