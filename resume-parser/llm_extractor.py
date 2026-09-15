import os
import json

from dotenv import load_dotenv
from groq import Groq

from models import Candidate

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_candidate(resume_text: str) -> Candidate:
    schema = json.dumps(Candidate.model_json_schema(), indent=2)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": f"""
You are a resume information extraction system.

Extract information from the resume and return JSON that STRICTLY matches this JSON Schema.
Use these exact field names — do not rename, omit, or restructure any field.

Schema:
{schema}

Rules:
- "experience" must be a list of objects with fields: title, company, description (description is a single string, not a list).
- "projects" must be a list of objects with fields: name, description.
- Return ONLY valid JSON. No markdown, no explanations, no extra fields.
"""
            },
            {
                "role": "user",
                "content": resume_text
            }
        ],
    )

    result = response.choices[0].message.content

    return Candidate.model_validate_json(result)
if __name__ == "__main__":
    from resume_parser import extract_resume_text

    text = extract_resume_text("resumes/sample_resume.pdf")

    candidate = extract_candidate(text)

    print(candidate.model_dump_json(indent=2))