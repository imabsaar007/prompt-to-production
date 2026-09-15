import sys

from resume_parser import extract_resume_text
from llm_extractor import extract_candidate
from hr_requirements import load_hr_requirements
from matcher import match_candidate


def print_report(candidate, requirements, match):
    print("=" * 50)
    print("CANDIDATE MATCH REPORT")
    print("=" * 50)

    print(f"\nCandidate: {candidate.name}")
    print(f"Email: {candidate.email}")
    print(f"Phone: {candidate.phone}")

    print(f"\nSkills found: {', '.join(candidate.skills)}")
    print(f"Skills required: {', '.join(requirements.skills)}")

    print(f"\n--- Match Scores ---")
    print(f"Skills Match:     {match.skills_match}%")
    print(f"Experience Match: {match.experience_match}%")
    print(f"Projects Match:   {match.projects_match}%")
    print(f"Overall Match:    {match.overall_match}%")
    print("=" * 50)


def run_pipeline(resume_path: str, hr_requirements_path: str = "hr_requirements.json"):
    print(f"Reading resume: {resume_path}")
    text = extract_resume_text(resume_path)

    print("Extracting candidate info...")
    candidate = extract_candidate(text)

    print("Loading HR requirements...")
    requirements = load_hr_requirements(hr_requirements_path)

    print("Matching candidate against requirements...\n")
    match = match_candidate(candidate, requirements)

    print_report(candidate, requirements, match)

    return candidate, requirements, match


if __name__ == "__main__":
    resume_path = sys.argv[1] if len(sys.argv) > 1 else "resumes/md_absaar_resume.pdf"
    run_pipeline(resume_path)