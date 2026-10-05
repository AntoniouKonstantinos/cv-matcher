import { useState } from "react";
import { uploadResume } from "../api";

function ResumeUpload({ onUploadSuccess }) {
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState(null);
    const [statusType, setStatusType] = useState(null);

    function handleFileChange(e) {
        setFile(e.target.files[0]);
    }

    async function handleSubmit(e) {
        e.preventDefault();

        if (!file) return;

        try {
            const data = await uploadResume(file);
            setStatus(`Uploaded: ${data.filename}`);
            setStatusType("success");
            onUploadSuccess(data.id);
        } catch (err) {
            setStatus(err.message);
            setStatusType("error");
        }
    }

    return (
        <section>
            <h2>1. Upload Resume</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="file"
                    accept=".pdf,.docx,.txt"
                    onChange={handleFileChange}
                    required
                />
                <button type="submit">Upload Resume</button>
            </form>
            {status && <p className={`status ${statusType}`}>{status}</p>}
        </section>
    );
}

export default ResumeUpload;