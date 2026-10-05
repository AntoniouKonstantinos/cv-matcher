import { useState } from "react";
import ResumeUpload from "./components/ResumeUpload";
import JobDescriptionForm from "./components/JobDescriptionForm";
import MatchScore from "./components/MatchScore";
import SkillsGapDashboard from "./components/SkillsGapDashboard";
import MatchHistory from "./components/MatchHistory";
import { runMatch } from "./api";
import "./styles/index.css";

function App() {
    const [resumeId, setResumeId] = useState(null);
    const [jobId, setJobId] = useState(null);
    const [matchResult, setMatchResult] = useState(null);
    const [isMatching, setIsMatching] = useState(false);
    const [matchError, setMatchError] = useState(null);
    const [historyRefreshKey, setHistoryRefreshKey] = useState(0);

    const canMatch = resumeId && jobId;

    async function handleRunMatch() {
        setIsMatching(true);
        setMatchError(null);

        try {
            const data = await runMatch(resumeId, jobId);
            setMatchResult(data);
            setHistoryRefreshKey((key) => key + 1);
        } catch (err) {
            setMatchError(err.message);
        } finally {
            setIsMatching(false);
        }
    }

    return (
        <main>
            <header>
                <h1>CV / Resume Matcher</h1>
                <p>Upload your resume, paste a job description, and see how well they match.</p>
            </header>

            <ResumeUpload onUploadSuccess={setResumeId} />
            <JobDescriptionForm onJobSaved={setJobId} />

            <section>
                <h2>3. Run Match</h2>
                <button onClick={handleRunMatch} disabled={!canMatch || isMatching}>
                    {isMatching ? "Matching..." : "Run Match"}
                </button>
                {matchError && <p className="status error">{matchError}</p>}

                {matchResult && (
                    <>
                        <MatchScore result={matchResult} />
                        <SkillsGapDashboard matchId={matchResult.id} />
                    </>
                )}
            </section>

            <MatchHistory refreshKey={historyRefreshKey} />
        </main>
    );
}

export default App;