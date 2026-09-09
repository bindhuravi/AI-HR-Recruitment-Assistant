import re
from src.models.schemas import JobDescription
from src.utils.file_loader import load_text_from_file
from src.tools.resume_parser_tool import SKILL_ALIASES

def _lines(block): return [re.sub(r'^[-•*]\s*','',x).strip() for x in block.splitlines() if x.strip()]
def _section(text, heading, next_headings):
    m=re.search(rf'(?is)^\s*{re.escape(heading)}\s*[:\-]?\s*(.*?)(?=^\s*(?:{next_headings})\s*[:\-]?\s*$|\Z)', text, re.M)
    return m.group(1).strip() if m else ''
def _skills(text):
    low=text.lower(); found=[]
    for name, aliases in SKILL_ALIASES.items():
        if any(a.strip().lower() in low for a in aliases): found.append(name)
    return found

def _canonical_skills(block):
    low=block.lower(); found=[]
    # Match the actual skill phrase while ignoring requirement wording.
    for name, aliases in SKILL_ALIASES.items():
        if any(a.strip().lower() in low for a in aliases): found.append(name)
    return found

def parse_job_description(file_path=None, raw_text=None):
    text=load_text_from_file(file_path) if file_path else (raw_text or '')
    lines=[x.strip() for x in text.splitlines() if x.strip()]
    title=lines[0] if lines else None
    cm=re.search(r'(?im)^company\s*:\s*(.+)$',text); company=cm.group(1).strip() if cm else None
    min_block=_section(text,'MINIMUM EXPERIENCE','RESPONSIBILITIES|QUALIFICATIONS|REQUIRED SKILLS|PREFERRED SKILLS')
    em=re.search(r'(\d+(?:\.\d+)?)\s*\+?\s*years?', min_block, re.I)
    exp=float(em.group(1)) if em else None
    req_block=_section(text,'REQUIRED SKILLS','PREFERRED SKILLS|MINIMUM EXPERIENCE|RESPONSIBILITIES|QUALIFICATIONS|ABOUT THE ROLE')
    pref_block=_section(text,'PREFERRED SKILLS','MINIMUM EXPERIENCE|RESPONSIBILITIES|QUALIFICATIONS|ABOUT THE ROLE')
    req=_canonical_skills(req_block)
    pref=_canonical_skills(pref_block)
    resp=_lines(_section(text,'RESPONSIBILITIES','QUALIFICATIONS|REQUIRED SKILLS|PREFERRED SKILLS|MINIMUM EXPERIENCE'))
    qual=_lines(_section(text,'QUALIFICATIONS','RESPONSIBILITIES|REQUIRED SKILLS|PREFERRED SKILLS|MINIMUM EXPERIENCE'))
    return JobDescription(title=title,company=company,required_skills=req or _skills(text),preferred_skills=pref,min_experience_years=exp,responsibilities=resp,qualifications=qual,raw_text=text).model_dump()
