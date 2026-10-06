function MatchScore({ result }) {
    const percentage = Math.round(result.similarity_score * 100);

    return (
        <div>
            <h3>Match Score</h3>
            <div className="score-display">{percentage}%</div>

            <div className="keywords">
                <div>
                    <h4>Matched Keywords</h4>
                    <ul>
                        {result.matched_keywords.map((kw) => (
                            <li key={kw} className="matched">
                                {kw}
                            </li>
                        ))}
                    </ul>
                </div>
                <div>
                    <h4>Missing Keywords</h4>
                    <ul>
                        {result.missing_keywords.map((kw) => (
                            <li key={kw} className="missing">
                                {kw}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default MatchScore;