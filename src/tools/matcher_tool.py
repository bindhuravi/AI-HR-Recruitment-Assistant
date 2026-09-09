from src.models.schemas import Candidate, JobDescription, MatchResult

def _norm(s):
    s=s.lower().strip()
    return {'rest api':'rest apis','restful api':'rest apis','postgres':'postgresql','microsoft excel':'excel','data analytics':'data analysis'}.get(s,s)
def skill_overlap(candidate_skills, required_skills):
    cand={_norm(s) for s in candidate_skills if s.strip()}; req={_norm(s) for s in required_skills if s.strip()}
    if not req:return 0.0,[],[]
    matched=req&cand; missing=req-cand
    return len(matched)/len(req)*100,sorted(matched),sorted(missing)
def experience_score(candidate_years,min_years):
    if not min_years:return 100.0
    if candidate_years is None:return 50.0
    if candidate_years>=min_years:return 100.0
    return max(0.0,candidate_years/min_years*100)
def match_candidate_to_job(candidate_json,job_description_json):
    c=Candidate(**candidate_json); j=JobDescription(**job_description_json)
    ss,matched,missing=skill_overlap(c.skills,j.required_skills); es=experience_score(c.total_experience_years,j.min_experience_years)
    overall=round(.7*ss+.3*es,1)
    strength=', '.join(matched[:5]) or 'few required skills'
    gap=', '.join(missing[:5]) or 'no major required-skill gaps'
    exp=f'{c.total_experience_years:g} years' if c.total_experience_years is not None else 'an unknown amount of experience'
    rationale=f'The candidate demonstrates {strength} and has {exp} of experience. The main gaps are {gap}. Based on the required-skill overlap and experience requirement, the calculated fit score is {overall}%.'
    return MatchResult(overall_score=overall,skill_match_score=round(ss,1),experience_match_score=round(es,1),matched_skills=matched,missing_skills=missing,rationale=rationale).model_dump()
