import os
from dotenv import load_dotenv
load_dotenv()
LLM_PROVIDER = "local"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESUME_DIR = os.path.join(DATA_DIR, "resumes")
JD_DIR = os.path.join(DATA_DIR, "job_descriptions")
KB_DIR = os.path.join(DATA_DIR, "knowledge_base")
VECTOR_DB_DIR = os.path.join(BASE_DIR, "local_index")
