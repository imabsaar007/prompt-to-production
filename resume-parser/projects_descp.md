# Resume Matcher

An LLM-powered pipeline that extracts structured candidate data from a resume (PDF/DOCX), compares it against HR-defined requirements, and generates a match score.

## How it works

1. **Extract text** from a resume file (PDF or DOCX)
2. **Parse it into structured JSON** (name, email, phone, skills, experience, projects) using an LLM via Groq
3. **Load HR requirements** (required skills, years of experience, project types) from a JSON file
4. **Match** the candidate against those requirements:
   - Skills → deterministic set overlap (case-insensitive)
   - Experience & Projects → LLM-based semantic judgment
5. **Print a report** with a skills/experience/projects/overall match percentage

## Project structure

```
resume-parser/
├── models.py              # Pydantic schemas: Candidate, HRRequirements, CandidateMatch, etc.
├── resume_parser.py        # Extracts raw text from PDF/DOCX resumes
├── llm_extractor.py         # Uses Groq LLM to turn resume text into a Candidate object
├── hr_requirements.py       # Loads HR requirements from hr_requirements.json
├── matcher.py                # Computes skills/experience/projects/overall match scores
├── main.py                    # Entry point — runs the full pipeline end-to-end
├── hr_requirements.json       # HR's required skills, experience years, project types
└── resumes/
    └── sample_resume.pdf       # Example resume input
```

## Setup

1. Install dependencies (via `uv` or `pip`):
   ```
   uv sync
   ```
   Required packages: `pydantic`, `pypdf`, `python-docx`, `groq`, `python-dotenv`

2. Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. Edit `hr_requirements.json` with the role's requirements:
   ```json
   {
     "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "REST APIs"],
     "experience_years": 2,
     "projects": ["REST API development", "LLM-based application"]
   }
   ```

## Usage

Run against the default sample resume:
```
uv run python main.py
```

Run against a specific resume:
```
uv run python main.py resumes/other_resume.pdf
```

### Example output

```
==================================================
CANDIDATE MATCH REPORT
==================================================

Candidate: Arjun Mehta
Email: arjun.mehta@example.com
Phone: +91 98765 43210

Skills found: Python, FastAPI, PostgreSQL, Docker, REST APIs
Skills required: Python, FastAPI, PostgreSQL, Docker, REST APIs

--- Match Scores ---
Skills Match:     100.0%
Experience Match: 85.0%
Projects Match:   90.0%
Overall Match:    91.67%
==================================================
```

## Design notes

- **Model**: uses Groq's `openai/gpt-oss-20b` for both extraction and semantic matching.
- **Schema enforcement**: the extraction prompt injects the Pydantic JSON schema directly (`Candidate.model_json_schema()`) to reduce field-naming drift from the LLM.
- **Hybrid matching**: skills are matched deterministically (fast, free, predictable) while experience/projects use LLM reasoning to catch semantic matches (e.g. "FastAPI REST API work" satisfying a "REST API development" requirement) that exact string matching would miss.

## Possible extensions

- Wrap the pipeline in error handling so a malformed resume or LLM hiccup doesn't crash the run
- Batch mode: process a folder of resumes and rank candidates by `overall_match`
- Export results to CSV/JSON instead of just printing
- Add a Streamlit front end for a visual demo