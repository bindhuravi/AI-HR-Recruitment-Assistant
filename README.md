# AI HR Recruitment Assistant — Local / No API Key

A Streamlit resume-screening application that runs entirely with local Python/NLP logic. No OpenAI, Anthropic, or paid API key is required.

## Features
- PDF/DOCX/TXT resume extraction
- Job-description parsing
- Skill matching and missing-skill detection
- Experience scoring
- 0–100 candidate fit score
- Technical, behavioral, and gap-probing interview questions
- Local keyword-based knowledge-base retrieval
- Animated White + Navy Blue Streamlit UI

## Run in VS Code
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m streamlit run app.py
```
Open `http://localhost:8501`.

## Important
This version deliberately removes cloud LLM/API dependencies. Results are deterministic and explainable, making it suitable for a college/portfolio demo. The existing animated UI is retained.
