from typing import List, Optional
from pydantic import BaseModel, Field
class Candidate(BaseModel):
    name: Optional[str]=None; email: Optional[str]=None; phone: Optional[str]=None
    total_experience_years: Optional[float]=None
    skills: List[str]=Field(default_factory=list); education: List[str]=Field(default_factory=list)
    work_history: List[str]=Field(default_factory=list); summary: Optional[str]=None; raw_text: str=""
class JobDescription(BaseModel):
    title: Optional[str]=None; company: Optional[str]=None
    required_skills: List[str]=Field(default_factory=list); preferred_skills: List[str]=Field(default_factory=list)
    min_experience_years: Optional[float]=None; responsibilities: List[str]=Field(default_factory=list)
    qualifications: List[str]=Field(default_factory=list); raw_text: str=""
class MatchResult(BaseModel):
    overall_score: float; skill_match_score: float; experience_match_score: float
    matched_skills: List[str]; missing_skills: List[str]; rationale: str
class InterviewQuestionSet(BaseModel):
    technical_questions: List[str]; behavioral_questions: List[str]; gap_probing_questions: List[str]
