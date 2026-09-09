import os

from pypdf import PdfReader
import docx


def load_text_from_file(file_path: str) -> str:
    """Load raw text from a .pdf, .docx, .txt or .md file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if ext == ".docx":
        document = docx.Document(file_path)
        return "\n".join(p.text for p in document.paragraphs)

    if ext in (".txt", ".md"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    raise ValueError(f"Unsupported file type: {ext}")
