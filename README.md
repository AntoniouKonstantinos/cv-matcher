# CV/Resume Matcher

A full-stack web application that analyzes how well a resume matches a job description using NLP techniques, and returns a similarity score along with matched and missing keywords.

Built as a hands-on exploration of applying text processing to a real-world problem: helping job seekers understand how their resume aligns with a specific job posting.

## Features

- **Upload resumes** in PDF, DOCX, or TXT format
- **Submit job descriptions** as plain text
- **NLP-based matching** using TF-IDF vectorization and cosine similarity
- **Keyword breakdown** showing which important terms from the job description are present in (or missing from) the resume
- **Match history** stored in a database, so past comparisons can be reviewed later
- **REST API** built with Flask, consumed by a vanilla JavaScript frontend

## Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy
- **NLP / Matching:** scikit-learn (TF-IDF, cosine similarity)
- **Text extraction:** pdfplumber (PDF), python-docx (DOCX)
- **Database:** SQLite (development), designed to be portable to PostgreSQL
- **Frontend:** Vanilla JavaScript, HTML, CSS

## How It Works

1. A user uploads a resume and pastes a job description.
2. The backend extracts raw text from the uploaded file.
3. Both texts are vectorized using **TF-IDF** (unigrams and bigrams), and compared using **cosine similarity** to produce a match score between 0 and 1.
4. The top TF-IDF-weighted keywords from the job description are checked against the resume text, producing lists of **matched** and **missing** keywords.
5. The result is stored in the database and returned to the frontend for display.

## Project Structure

```
cv-matcher/
├── app/
│   ├── __init__.py       # Flask application factory
│   ├── models.py         # Database models (Resume, JobDescription, MatchResult)
│   ├── routes.py         # API endpoints
│   ├── extraction.py     # Text extraction from PDF/DOCX/TXT
│   └── matching.py       # TF-IDF + cosine similarity logic
├── static/                # CSS and JavaScript
├── templates/              # HTML templates
├── tests/                 # Unit tests
├── config.py               # App configuration
├── run.py                  # Application entry point
└── requirements.txt
```

## API Endpoints

| Method | Endpoint              | Description                              |
|--------|------------------------|-------------------------------------------|
| POST   | `/api/resumes`         | Upload a resume file                      |
| POST   | `/api/jobs`             | Submit a job description                  |
| POST   | `/api/match`             | Run a match between a resume and a job    |
| GET    | `/api/matches`           | List match history                        |
| GET    | `/api/matches/<id>`       | Get details of a specific match           |
| GET    | `/api/resumes/<id>`       | View extracted text of a resume           |
| GET    | `/api/jobs/<id>`           | View a stored job description             |

## Setup

```bash
# Clone the repository
git clone https://github.com/AntoniouKonstantinos/cv-matcher.git
cd cv-matcher

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create required folders
mkdir instance uploads

# Run the app
python run.py
```

The app will be available at `http://localhost:5000`.

## Why This Project

This project was built to practice combining classical NLP techniques (TF-IDF, cosine similarity) with a full-stack application, going beyond tutorial-style projects by tackling a real, practical problem: helping people understand and improve how their resume matches a specific job posting.

## Future Improvements

- Support for more nuanced matching (e.g. synonym awareness, skill taxonomies)
- User accounts to track match history per person
- Resume improvement suggestions based on missing keywords
- Support for multiple job descriptions compared against one resume

## License

MIT
