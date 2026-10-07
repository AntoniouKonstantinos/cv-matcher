import { useState, useEffect } from "react";
import { getMatchHistory } from "../api";

function MatchHistory({ refreshKey }) {
    const [matches, setMatches] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        let cancelled = false;

        async function loadHistory() {
            setLoading(true);
            setError(null);

            try {
                const data = await getMatchHistory();
                if (!cancelled) {
                    setMatches(data.matches);
                }
            } catch (err) {
                if (!cancelled) {
                    setError(err.message);
                }
            } finally {
                if (!cancelled) {
                    setLoading(false);
                }
            }
        }

        loadHistory();

        return () => {
            cancelled = true;
        };
    }, [refreshKey]);

    return (
        <section>
            <h2>Match History</h2>

            {loading && <p>Loading history...</p>}
            {error && <p className="status error">{error}</p>}

            {!loading && !error && (
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Score</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {matches.map((m) => (
                            <tr key={m.id}>
                                <td>{m.id}</td>
                                <td>{Math.round(m.similarity_score * 100)}%</td>
                                <td>{new Date(m.created_at).toLocaleDateString()}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </section>
    );
}

export default MatchHistory;