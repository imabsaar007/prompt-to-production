from pydantic import BaseModel


class Experience(BaseModel):
    title: str
    company: str
    description: str


class Project(BaseModel):
    name: str
    description: str


class Candidate(BaseModel):
    name: str
    email: str
    phone: str
    skills: list[str]
    experience: list[Experience]   # was list[str]
    projects: list[Project]        # was list[str]


class HRRequirements(BaseModel):
    skills: list[str]
    experience_years: int
    projects: list[str]


class CandidateMatch(BaseModel):
    skills_match: float
    experience_match: float
    projects_match: float
    overall_match: float