import asyncio
from sqlalchemy import select

from app.database import AsyncSessionLocal, init_db
from app.models import Skill

SKILLS = {
    'language': [
        'Python', 'JavaScript', 'TypeScript', 'Java', 'C#', 'C++', 'PHP',
        'Golang', 'Rust', 'Kotlin', 'Swift', 'Ruby', 'SQL', 'HTML', 'CSS',
        'Bash', 'R programming',
    ],
    'framework': [
        'Flask', 'FastAPI', 'Django', 'React', 'Angular', 'Vue.js', 'Node.js',
        'Express.js', 'Next.js', 'Spring Boot', 'ASP.NET', 'Laravel',
        'Bootstrap', 'Tailwind CSS', 'jQuery', 'Redux', 'RxJS', 'SQLAlchemy',
        'Hibernate', 'pytest', 'JUnit', 'scikit-learn', 'TensorFlow',
        'PyTorch', 'Pandas', 'NumPy',
    ],
    'database': [
        'PostgreSQL', 'MySQL', 'SQLite', 'MongoDB', 'Redis',
        'Microsoft SQL Server', 'Oracle Database', 'Elasticsearch',
        'Firebase', 'DynamoDB',
    ],
    'tool': [
        'Git', 'GitHub', 'GitLab', 'Docker', 'Kubernetes', 'Jenkins',
        'GitHub Actions', 'AWS', 'Microsoft Azure', 'Google Cloud Platform',
        'Linux', 'Nginx', 'Postman', 'Jira', 'Terraform', 'npm', 'Webpack',
        'Figma', 'Power BI', 'Tableau', 'Jupyter Notebook',
    ],
    'concept': [
        'REST API', 'GraphQL', 'CI/CD', 'DevOps', 'Agile', 'Scrum',
        'Test-driven development', 'Unit testing', 'Object-oriented programming',
        'Microservices', 'Design patterns', 'Data structures and algorithms',
        'Code review', 'Version control', 'Machine learning', 'Data analysis',
        'Web security', 'Authentication and authorization',
        'Responsive design', 'Database design',
    ],
    'soft_skill': [
        'Leadership', 'Communication', 'Teamwork', 'Collaboration',
        'Problem solving', 'Critical thinking', 'Analytical thinking',
        'Time management', 'Adaptability', 'Attention to detail',
        'Customer service', 'Project management', 'Mentoring', 'Creativity',
        'Stakeholder management', 'Ownership',
    ],
}


async def seed_skills():
    await init_db()

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Skill.name))
        existing_names = set(result.scalars().all())

        added = 0
        for category, names in SKILLS.items():
            for name in names:
                if name in existing_names:
                    continue
                session.add(Skill(name=name, category=category))
                added += 1

        await session.commit()

    print(f"Seed complete: {added} new skills added, {len(existing_names)} already existed.")


if __name__ == '__main__':
    asyncio.run(seed_skills())