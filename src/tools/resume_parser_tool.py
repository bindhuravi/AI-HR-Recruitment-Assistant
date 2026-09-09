import re
from src.models.schemas import Candidate
from src.utils.file_loader import load_text_from_file

SKILL_ALIASES = {
    "python":["python"],"go":["go"],"java":["java"],"c":["c programming"],"c++":["c++"],"sql":["sql"],
    "power bi":["power bi"],"excel":["excel","microsoft excel"],"power query":["power query"],
    "pandas":["pandas"],"numpy":["numpy"],"scikit-learn":["scikit-learn","sklearn"],"tensorflow":["tensorflow"],
    "pytorch":["pytorch"],"aws":["aws"],"azure":["azure"],"gcp":["gcp"],"docker":["docker"],"kubernetes":["kubernetes"],
    "git":["git"],"rest apis":["rest api","restful api","rest apis"],"django":["django"],"fastapi":["fastapi"],
    "flask":["flask"],"postgresql":["postgresql","postgres"],"mysql":["mysql"],"mongodb":["mongodb"],"redis":["redis"],
    "kafka":["kafka"],"html":["html"],"css":["css"],"javascript":["javascript"],"prompt engineering":["prompt engineering"],
    "data analysis":["data analysis","data analytics"],"data visualization":["data visualization"],"machine learning":["machine learning"],
}
def _skills(text):
    low=text.lower(); found=[]
    for name, aliases in SKILL_ALIASES.items():
        if any(a.strip() in low for a in aliases): found.append(name)
    return found
def _experience(text):
    m=re.search(r'(\d+(?:\.\d+)?)\s*\+?\s*years?\s*(?:of\s*)?(?:professional|work|industry)?\s*(?:backend|engineering|software)?\s*experience', text, re.I)
    if m: return float(m.group(1))
    years=[]
    for a,b in re.findall(r'\b(19\d{2}|20\d{2})\s*[-–]\s*(Present|19\d{2}|20\d{2})\b',text,re.I):
        end=2026 if b.lower()=='present' else int(b); years.append(max(0,end-int(a)))
    return float(max(years)) if years else None
def _section(text, heading, next_headings):
    m=re.search(rf'(?is)^\s*{re.escape(heading)}\s*[:\-]?\s*\n?(.*?)(?=^\s*(?:{next_headings})\s*[:\-]?\s*$|\Z)', text, re.M)
    return m.group(1).strip() if m else ''
def _lines(block): return [re.sub(r'^[-•*]\s*','',x).strip() for x in block.splitlines() if x.strip()]
def parse_resume(file_path: str) -> dict:
    text=load_text_from_file(file_path); lines=[x.strip() for x in text.splitlines() if x.strip()]
    email=(re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',text) or [None])[0]
    phone=(re.search(r'(?:\+?\d[\d\s().-]{7,}\d)',text) or [None])[0]
    name=lines[0] if lines and not re.search(r'@|resume|curriculum',lines[0],re.I) else None
    education=_lines(_section(text,'EDUCATION','SUMMARY|SKILLS|WORK HISTORY|EXPERIENCE|PROJECTS|WORK EXPERIENCE'))
    work=_lines(_section(text,'WORK HISTORY','EDUCATION|SKILLS|SUMMARY|PROJECTS|QUALIFICATIONS'))
    if not work: work=_lines(_section(text,'WORK EXPERIENCE','EDUCATION|SKILLS|SUMMARY|PROJECTS|QUALIFICATIONS'))
    summary=_section(text,'SUMMARY','SKILLS|WORK HISTORY|WORK EXPERIENCE|EDUCATION|PROJECTS') or None
    skills=_skills(text)
    return Candidate(name=name,email=email,phone=phone,total_experience_years=_experience(text),skills=skills,education=education,work_history=work,summary=summary or (lines[1] if len(lines)>1 else None),raw_text=text).model_dump()
