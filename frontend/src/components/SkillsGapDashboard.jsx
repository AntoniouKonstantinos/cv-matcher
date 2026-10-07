import { useState, useEffect } from "react";
import { getSkillsGap } from "../api";

function SkillsGapDashboard({ matchId }) {
    const [skills, setSkills] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        let cancelled = false;

        async function loadSkillsGap() {
            setLoading(true);
            setError(null);

            try {
                const data = await getSkillsGap(matchId);
                if (!cancelled) {
                    setSkills(data.skills);
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

        loadSkillsGap();

        return () => {
            cancelled = true;
        };
    }, [matchId]);

    if (loading) {
        return <p>Loading skills breakdown...</p>;
    }

    if (error) {
        return <p className="status error">{error}</p>;
    }

    if (skills.length === 0) {
        return null;
    }

    const grouped = skills.reduce((acc, skill) => {
        if (!acc[skill.category]) {
            acc[skill.category] = [];
        }
        acc[skill.category].push(skill);
        return acc;
    }, {});

    return (
        <div>
            <h3>Skills Breakdown</h3>
            {Object.entries(grouped).map(([category, categorySkills]) => (
                <div key={category}>
                    <h4>{category}</h4>
                    <ul className="skills-list">
                        {categorySkills.map((skill) => (
                            <li
                                key={skill.skill_name}
                                className={skill.present_in_resume ? "skill-present" : "skill-missing"}
                            >
                                {skill.skill_name}
                                <span className="confidence">
                                    {Math.round(skill.confidence_score * 100)}%
                                </span>
                            </li>
                        ))}
                    </ul>
                </div>
            ))}
        </div>
    );
}

export default SkillsGapDashboard;