from src.models.schemas import Candidate, JobDescription, InterviewQuestionSet

def generate_interview_questions(candidate_json,job_description_json):
    c=Candidate(**candidate_json); j=JobDescription(**job_description_json); gaps=[]
    for s in j.required_skills:
        if s.lower().strip() not in {x.lower().strip() for x in c.skills}: gaps.append(s)
    role=j.title or 'this role'; skills=j.required_skills[:4] or c.skills[:4]
    technical=[f'How have you used {s} in a real project, and what trade-offs did you consider?' for s in skills]
    technical=(technical+[f'Describe a challenging {role} problem you solved and how you validated the solution.'])[:4]
    behavioral=['Tell me about a time you disagreed with a teammate. How did you resolve it?', 'Describe a project that went wrong. What did you learn?', 'How do you prioritize when several important tasks are urgent?']
    gap=[f'This role requires {g}. How would you approach becoming productive with it?' for g in gaps[:2]]
    if not gap: gap=['Describe an area of the role where you would need the most onboarding and how you would close that gap.', 'What would you improve in one of your recent projects if you had another month?']
    return InterviewQuestionSet(technical_questions=technical,behavioral_questions=behavioral,gap_probing_questions=gap).model_dump()
