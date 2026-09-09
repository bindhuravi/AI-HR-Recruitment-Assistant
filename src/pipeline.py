from src.tools.resume_parser_tool import parse_resume
from src.tools.jd_parser_tool import parse_job_description
from src.tools.matcher_tool import match_candidate_to_job
from src.tools.question_generator_tool import generate_interview_questions

def screen_candidate(resume_path,jd_path):
    candidate=parse_resume(resume_path); jd=parse_job_description(file_path=jd_path)
    match=match_candidate_to_job(candidate,jd); questions=generate_interview_questions(candidate,jd)
    return {'candidate':candidate,'job_description':jd,'match':match,'interview_questions':questions}
