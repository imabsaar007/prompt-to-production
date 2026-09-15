import os
import json

from dotenv import load_dotenv
from groq import Groq

from models import Candidate, HRRequirements, CandidateMatch

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def compute_skills_match(candidate_skills: list[str], required_skills: list[str]) -> float:
    if not required_skills:
        return 100.0

    candidate_set = {s.strip().lower() for s in candidate_skills}
    required_set = {s.strip().lower() for s in required_skills}

    matched = candidate_set & required_set

    return round(len(matched) / len(required_set) * 100, 2)


def compute_semantic_match(candidate: Candidate, requirements: HRRequirements) -> dict:
    """Ask the LLM to judge experience_match and projects_match (0-100)."""

    candidate_experience = [exp.model_dump() for exp in candidate.experience]
    candidate_projects = [proj.model_dump() for proj in candidate.projects]

    prompt = f"""
Candidate experience:
{json.dumps(candidate_experience, indent=2)}

Candidate projects:
{json.dumps(candidate_projects, indent=2)}

HR required experience years: {requirements.experience_years}
HR required project types: {requirements.projects}

Judge how well the candidate's experience and projects match the HR requirements.
Consider semantic closeness, not just exact wording (e.g. "FastAPI REST API" counts toward "REST API development").

Return ONLY valid JSON in this exact shape, no markdown, no explanation:
{{
  "experience_match": <float 0-100>,
  "projects_match": <float 0-100>
}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You are a strict but fair HR matching assistant. Return only JSON."},
            {"role": "user", "content": prompt}
        ],
    )

    result = response.choices[0].message.content
    return json.loads(result)


def match_candidate(candidate: Candidate, requirements: HRRequirements) -> CandidateMatch:
    skills_match = compute_skills_match(candidate.skills, requirements.skills)
    semantic = compute_semantic_match(candidate, requirements)

    experience_match = semantic["experience_match"]
    projects_match = semantic["projects_match"]

    overall_match = round(
        (skills_match + experience_match + projects_match) / 3, 2
    )

    return CandidateMatch(
        skills_match=skills_match,
        experience_match=experience_match,
        projects_match=projects_match,
        overall_match=overall_match,
    )


if __name__ == "__main__":
    from resume_parser import extract_resume_text
    from llm_extractor import extract_candidate
    from hr_requirements import load_hr_requirements

    text = extract_resume_text("resumes/engineering-resume-example.pdf")
    candidate = extract_candidate(text)
    requirements = load_hr_requirements("hr_requirements.json")

    match = match_candidate(candidate, requirements)
    print(match.model_dump_json(indent=2))